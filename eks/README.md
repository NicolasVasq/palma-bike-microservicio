# Despliegue en Amazon EKS

Fase 2 del Examen Final Transversal: el microservicio Palma Bike desplegado en
Kubernetes gestionado por AWS (EKS Auto Mode), sobre la cuenta de AWS Academy.

## Archivos

| Archivo | Propósito |
|---|---|
| `cluster.yaml` | Definición del clúster (eksctl): EKS Auto Mode, rol de clúster pre-aprovisionado por el lab, logs del control plane en CloudWatch |
| `storageclass.yml` | StorageClass gp3 (default) con el driver EBS CSI de Auto Mode; sin ella el PVC queda Pending |
| `deploy_eks.sh` | Ciclo completo: clúster → kubeconfig → metrics-server → manifiestos → secreto → pruebas de aceptación contra el balanceador |
| `destroy_eks.sh` | Destruye el clúster para detener la facturación |

## Prerequisitos

```bash
export AWS_ACCESS_KEY_ID=...      # credenciales temporales del Learner Lab
export AWS_SECRET_ACCESS_KEY=...
export AWS_SESSION_TOKEN=...
export AWS_REGION=us-west-2
```

Herramientas: `aws` (CLI), `eksctl`, `kubectl`, `openssl`, Python 3.

## Ciclo de vida (disciplina de costo)

```bash
bash eks/deploy_eks.sh     # crear/verificar + desplegar + aceptación (~20 min)
# ... capturar evidencia, demostrar ...
bash eks/destroy_eks.sh   # destruir SIEMPRE al terminar (~10 min)
```

**Por qué destruir siempre:** el plano de control de EKS factura ~US$0.10/hora
aunque nadie lo use (~US$2.4/día). Con el presupuesto de AWS Academy esto es
insostenible; además el despliegue completo toma ~20 minutos con el script,
así que recrearlo para una demostración es trivial.

**Costo de una sesión de 8 horas** ≈ US$1.50–2.00 (control plane + nodos Auto
Mode + 1 Gi gp3).

## Despliegue verificado (2026-11-27)

- Clúster `palma-bike` en `us-west-2`, Kubernetes 1.37, **EKS Auto Mode**.
- 2 réplicas del microservicio `Running` en 2 nodos gestionados por Auto Mode.
- NLB **internet-facing** (ver gotcha abajo) publicado en DNS público.
- PVC de SQLite `Bound` a un volumen gp3 de 1 Gi (EBS CSI de Auto Mode).
- HPA reportando métricas reales vía metrics-server (addon EKS).
- Logs del control plane fluyendo a CloudWatch Logs.
- **Pruebas de aceptación 5/5 PASS** contra la URL del balanceador.

## Restricciones del AWS Academy Learner Lab y cómo se resolvieron

| Restricción | Solución aplicada |
|---|---|
| `iam:CreateRole` denegado (eksctl no puede crear roles) | Se usan los roles pre-aprovisionados por Vocareum: `LabEksClusterRole` (con las políticas de Auto Mode) vía `iam.serviceRoleARN` y `LabEksNodeRole` vía `autoModeConfig.nodeRoleARN` |
| Sin OIDC/IRSA (no se pueden crear roles para addons) | EKS Auto Mode gestiona EBS y balanceadores desde el propio servicio EKS, sin roles del usuario |
| Sin perfiles de instancia para nodos propios | Auto Mode gestiona los nodos; EKS no necesita perfiles del usuario |
| Sin IAM para CloudWatch Container Insights (requiere IRSA) | Se documenta el límite; la evidencia de métricas usa CloudWatch del NLB/EC2 y los logs del control plane |

## Decisiones de seguridad documentadas

- **TLS en el balanceador:** el NLB publica el servicio por HTTP (puerto 80).
  Terminar TLS requeriría un certificado ACM con validación DNS, inviable con
  el hostname efímero del balanceador de un clúster de vida corta. En un
  despliegue real con dominio propio, el paso sería solicitar el ACM cert y
  anotar el Service con `aws-load-balancer-ssl-cert` + puerto 443.
- **Container Insights:** no se activa porque requiere IRSA (crear roles IAM
  para el agente de CloudWatch), bloqueado por el Learner Lab. La evidencia
  de métricas usa los namespaces NLB/EC2 de CloudWatch y los logs del
  control plane.

## Gotchas de EKS Auto Mode descubiertos

1. **El Service type LoadBalancer crea un NLB interno por defecto**: hay que
   anotar el Service con `aws-load-balancer-scheme: internet-facing`
   (incorporado en `k8s/06-service.yml`).
2. **No existe StorageClass default**: un PVC sin `storageClassName` queda
   `Pending`; `eks/storageclass.yml` declara gp3 como default.
3. **El DNS del NLB nuevo tarda 1–5 min en publicarse**: `deploy_eks.sh`
   espera la resolución antes de correr las pruebas de aceptación.
4. **Windows (PowerShell sin admin)**: el launcher `aws.cmd` de awscli v1
   instalado por pip es defectuoso; si kubectl no puede obtener el token del
   clúster, editar `~/.kube/config` y reemplazar el `command: aws` del bloque
   `exec` por el intérprete de Python del venv con un `-c` que invoque
   `awscli.clidriver` (así queda registrado en este proyecto).

## Qué capturar como evidencia del ET

1. Consola AWS → EKS → clúster `palma-bike`: overview, compute (nodos), addons
2. EKS → Resources → Workloads: deployment `palma-bike` con 2 pods
3. EC2 → Load Balancers: NLB con scheme `internet-facing`
4. EC2 → Volumes: volumen gp3 de 1 Gi del PVC
5. CloudWatch → Log Groups: `/aws/eks/palma-bike/cluster` (logging del control plane)
6. CloudWatch → Metrics → namespace ELB: RequestCount del balanceador
7. La URL del balanceador cargando la tienda en el navegador
8. `kubectl get hpa -n palma-bike` con métricas en vivo

## Notas técnicas

- **Secreto de Django:** `03-secret.yml` queda como documentación; el secreto
  real se crea con `kubectl create secret generic --dry-run` (clave generada
  con `openssl rand`), nunca versionada.
- **metrics-server:** EKS no lo incluye en clústeres clásicos y el HPA lo
  necesita; en este clúster lo instala eksctl como addon automáticamente y
  `deploy_eks.sh` lo verifica/instala como manifiesto si no existe.
- **Credenciales del Learner Lab:** vencen cada ~4 horas; renovarlas es solo
  volver a abrir el lab y actualizar las variables de entorno. No representan
  un problema para el clúster, que vive en la cuenta AWS.
