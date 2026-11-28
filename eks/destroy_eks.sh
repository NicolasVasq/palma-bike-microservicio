#!/usr/bin/env bash
# Destruye el cluster EKS de Palma Bike para detener la facturacion.
# El control plane de EKS cobra ~US$0.10/hora mientras el cluster exista.
#
# Uso:  bash eks/destroy_eks.sh
set -euo pipefail

REGION="${AWS_REGION:-us-west-2}"
CLUSTER="palma-bike"

if ! eksctl get cluster --name "$CLUSTER" --region "$REGION" >/dev/null 2>&1; then
  echo "No hay cluster '$CLUSTER' en $REGION, nada que destruir."
  exit 0
fi

echo "Destruyendo cluster $CLUSTER (incluye nodegroups, VPC y roles IAM)..."
eksctl delete cluster --name "$CLUSTER" --region "$REGION" --wait

echo ""
echo "Cluster destruido. Verifica en la consola AWS:"
echo "  - CloudFormation: no queden stacks en estado DELETE_FAILED"
echo "  - EC2 > Load Balancers: el balanceador debe desaparecer solo"
echo "  - VPC: las subnets creadas por eksctl deben eliminarse"
