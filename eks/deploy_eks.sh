#!/usr/bin/env bash
# Despliegue de Palma Bike en Amazon EKS.
#
# Prerequisitos (variables de entorno):
#   AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY / AWS_SESSION_TOKEN
#   AWS_REGION (opcional, por defecto us-east-1)
#   PYTHON (opcional, interprete para las pruebas de aceptacion)
#
# Uso:  bash eks/deploy_eks.sh
set -euo pipefail

REGION="${AWS_REGION:-us-west-2}"
CLUSTER="palma-bike"
NAMESPACE="palma-bike"
K8S_DIR="$(cd "$(dirname "$0")/../k8s" && pwd)"

echo "== 1/6 Verificando credenciales AWS =="
aws sts get-caller-identity

echo "== 2/6 Creando cluster EKS (o reutilizando el existente) =="
if eksctl get cluster --name "$CLUSTER" --region "$REGION" >/dev/null 2>&1; then
  echo "El cluster ya existe, se reutiliza."
else
  eksctl create cluster -f eks/cluster.yaml --wait
fi

echo "== 3/6 Verificando kubeconfig =="
if ! kubectl get ns >/dev/null 2>&1; then
  eksctl utils write-kubeconfig --cluster "$CLUSTER" --region "$REGION" --set-context auto
fi
kubectl get ns >/dev/null 2>&1 || { echo "ERROR: kubeconfig no funcional."; exit 1; }

echo "== 4/6 metrics-server (requerido por el HPA) =="
if kubectl get deployment metrics-server -n kube-system >/dev/null 2>&1; then
  echo "metrics-server ya instalado en el cluster, se omite."
else
  kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
  kubectl rollout status deployment/metrics-server -n kube-system --timeout=300s
fi

echo "== 5/6 Aplicando manifiestos y secreto de la aplicacion =="
kubectl apply -f "$K8S_DIR/01-namespace.yml"
kubectl apply -f "$K8S_DIR/02-configmap.yml"
kubectl apply -f "$K8S_DIR/04-pvc.yml"
kubectl apply -f "$K8S_DIR/05-deployment.yml"
kubectl apply -f "$K8S_DIR/06-service.yml"
kubectl apply -f "$K8S_DIR/07-hpa.yml"

SECRET_KEY_EKS="$(openssl rand -base64 48)"
kubectl create secret generic palma-bike-secrets \
  --namespace "$NAMESPACE" \
  --from-literal="SECRET_KEY=$SECRET_KEY_EKS" \
  --dry-run=client -o yaml | kubectl apply -f -

kubectl rollout status deployment/palma-bike -n "$NAMESPACE" --timeout=600s

echo "== 6/6 Esperando LoadBalancer y ejecutando pruebas de aceptacion =="
LB_HOSTNAME=""
for i in $(seq 1 30); do
  LB_HOSTNAME="$(kubectl get svc palma-bike -n "$NAMESPACE" -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')"
  [ -n "$LB_HOSTNAME" ] && break
  echo "  Esperando hostname del balanceador... ($i/30)"
  sleep 10
done
if [ -z "$LB_HOSTNAME" ]; then
  echo "ERROR: el servicio no obtuvo hostname de LoadBalancer."
  exit 1
fi

LB_URL="http://$LB_HOSTNAME"
echo "Servicio expuesto en: $LB_URL"

PY="${PYTHON:-python3}"
command -v "$PY" >/dev/null 2>&1 || PY="python"

echo "Esperando publicacion DNS del balanceador (max 6 min)..."
DNS_OK=0
for i in $(seq 1 12); do
  if "$PY" -c "import socket; socket.gethostbyname('$LB_HOSTNAME')" >/dev/null 2>&1; then
    DNS_OK=1
    echo "  DNS resolvio en intento $i"
    break
  fi
  echo "  Aun no resuelve... ($i/12)"
  sleep 30
done
if [ "$DNS_OK" != "1" ]; then
  echo "ERROR: el DNS del balanceador no resolvio a tiempo."
  exit 1
fi

BASE_URL="$LB_URL" "$PY" scripts/acceptance_tests.py

echo ""
echo "Despliegue completado. Pruebas de aceptacion superadas contra EKS."
echo "Recuerda destruir el cluster al terminar: bash eks/destroy_eks.sh"
