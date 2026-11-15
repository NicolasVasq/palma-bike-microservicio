# Despliegue orquestado en Kubernetes

Esta carpeta contiene los manifiestos para desplegar el microservicio Palma Bike en un clúster de Kubernetes.

## Estructura

- `01-namespace.yml`: crea el namespace `palma-bike`.
- `02-configmap.yml`: variables de entorno no sensibles.
- `03-secret.yml`: credenciales y llave secreta (reemplazar antes de producción).
- `05-deployment.yml`: despliegue con 2 réplicas, healthchecks y recursos.
- `06-service.yml`: servicio de tipo LoadBalancer.
- `07-hpa.yml`: autoescalado horizontal según CPU y memoria.

## Instrucciones

Requisitos: `kubectl` configurado contra un clúster (EKS, GKE, AKS, minikube, kind, etc.).

```bash
kubectl apply -f k8s/
```

Monitorear el despliegue:

```bash
kubectl get pods -n palma-bike -w
kubectl logs -n palma-bike -l app=palma-bike
```

Exponer el servicio localmente (minikube o similar):

```bash
kubectl port-forward -n palma-bike svc/palma-bike 8080:80
```

Abrir http://localhost:8080.

## Notas

- El manifiesto de `Secret` incluye un placeholder. En producción generarlo con:
  `kubectl create secret generic palma-bike-secrets --from-literal=SECRET_KEY='<valor>' -n palma-bike`.
- La imagen referenciada es `nicolasvasq/palma-bike-microservicio:latest`. Asegurar que el pipeline la publique en un registro accesible.
