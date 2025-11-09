# Kubernetes Deployment Guide

## Prerequisites

- Kubernetes cluster 1.20+
- kubectl configured
- Helm 3.0+ (optional)

## Quick Deployment

```bash
# Apply manifests
kubectl apply -f k8s/

# Check status
kubectl get pods -l app=vmware-vcf-architecture
```

## Configuration

### Secrets

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: vcf-credentials
type: Opaque
stringData:
  endpoint: https://vcf.example.com
  username: admin@vsphere.local
  password: SecurePassword123!
```

### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vmware-vcf-architecture
spec:
  replicas: 3
  selector:
    matchLabels:
      app: vmware-vcf-architecture
  template:
    spec:
      containers:
      - name: vcf-architecture
        image: ghcr.io/uldyssian-sh/vmware-vcf-architecture:latest
        ports:
        - containerPort: 8080
        env:
        - name: VCF_ENDPOINT
          valueFrom:
            secretKeyRef:
              name: vcf-credentials
              key: endpoint
```

## Monitoring

- Prometheus metrics on port 9090
- Health checks on /health endpoint
- Grafana dashboards available# Updated 20251109_123823
