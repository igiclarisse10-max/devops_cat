# Deployment Guide

This document covers deploying the `todo-app` to Kubernetes (recommended) and Docker Swarm (alternative). It also describes rolling updates, blue-green deployment, and resource sizing recommendations.

## Quick start (Kubernetes)

Prerequisites:
- A Kubernetes cluster (minikube, k3s, GKE, EKS, AKS, etc.)
- `kubectl` configured and pointing to your cluster
- Docker Hub credentials (or another registry) and image pushed

Steps:

1. Build and push the image locally (optional if CI does it):
```bash
VERSION=$(cat VERSION)
docker build -t YOUR_DOCKERHUB_USERNAME/todo-app:$VERSION --build-arg VERSION="$VERSION" .
docker push YOUR_DOCKERHUB_USERNAME/todo-app:$VERSION
docker tag YOUR_DOCKERHUB_USERNAME/todo-app:$VERSION YOUR_DOCKERHUB_USERNAME/todo-app:latest
docker push YOUR_DOCKERHUB_USERNAME/todo-app:latest
```

2. Update `k8s/deployment.yaml` to point at your image (or use `kubectl set image` as in the CI workflow):
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
```

3. Monitor rollout:
```bash
kubectl rollout status deployment/todo-app
kubectl get pods -l app=todo-app
kubectl get hpa
```

## Blue/Green deployment (manual)

1. Apply both deployments in `k8s/blue-green.yaml` (it creates `todo-app-blue` and `todo-app-green` and a service pointing to `active: blue`):
```bash
kubectl apply -f k8s/blue-green.yaml
```

2. Deploy new image to the idle color (e.g., green) by updating the green deployment image:
```bash
kubectl set image deployment/todo-app-green todo-app=YOUR_DOCKERHUB_USERNAME/todo-app:<new-tag>
kubectl rollout status deployment/todo-app-green
```

3. Verify the green deployment is healthy, then swap the service selector:
```bash
# Toggle with the provided script
chmod +x k8s/swap-blue-green.sh
./k8s/swap-blue-green.sh default todo-app-service
```

4. Optionally scale down the old color or keep it for quick rollback.

## Rolling Updates

The `k8s/deployment.yaml` uses a RollingUpdate strategy with:
- `maxUnavailable: 25%` — keeps most pods available during updates
- `maxSurge: 25%` — allows some new pods to be created above desired count

This provides a smooth upgrade with minimal downtime.

## Resource Requirements & Sizing

These are recommendations based on a small Flask app with light CPU usage and minimal memory footprint.

Baseline per-replica (small production):
- CPU request: 200m (0.2 CPU)
- CPU limit: 500m (0.5 CPU)
- Memory request: 256Mi
- Memory limit: 512Mi

How to calculate:
- Average request CPU time ~ 50ms on 1 CPU => 0.05 CPU per request
- If you expect 20 RPS sustained, CPU required ≈ 20 * 0.05 = 1.0 CPU
- With requests set to 200m per pod, you'd need 5 pods to handle 20 RPS.

Example for 100 RPS:
- Required CPU ≈ 100 * 0.05 = 5 CPU
- With 0.5 CPU limit per pod, use at least 10 pods (or increase per-pod limits).

Memory sizing:
- Flask baseline memory ~50-100MB per process (varies by libs)
- With buffer and traffic, 256Mi request is a safe starting point for basic workloads.

Horizontal scaling:
- Use the HPA (`k8s/hpa.yaml`) to autoscale by CPU (50% target). Tune thresholds based on actual metrics.

## Docker Swarm (alternative)

1. Initialize Swarm or join an existing one.
2. Build and push image as described above.
3. Example `docker-compose-swarm.yml` (create if you want Swarm):
```yaml
version: '3.8'
services:
  todo-app:
    image: YOUR_DOCKERHUB_USERNAME/todo-app:latest
    ports:
      - 80:5000
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.2'
          memory: 256M
```

Deploy on swarm:
```bash
docker stack deploy -c docker-compose-swarm.yml todo-app-stack
```

## CI/CD Integration

The provided `.github/workflows/cd.yml` will:
- Build and push the Docker image to Docker Hub (requires `DOCKER_HUB_USERNAME` and `DOCKER_HUB_PASSWORD` secrets)
- Use a `KUBE_CONFIG` secret (base64-encoded kubeconfig) to apply the manifest or set the image

### Secrets required for CD workflow
- `DOCKER_HUB_USERNAME` and `DOCKER_HUB_PASSWORD`
- `KUBE_CONFIG` (base64-encoded content of your kubeconfig: `cat ~/.kube/config | base64 -w0`)

## Rollback

- For rolling updates, use `kubectl rollout undo deployment/todo-app`.
- For blue/green, switch the service selector back to the previous color.

## Monitoring

- Integrate Prometheus/Grafana for CPU/memory/latency metrics.
- Use logs (Fluentd/Elastic/LogDNA) to capture application logs.

## Next Steps

- Add readiness endpoint that checks DB connectivity to avoid routing traffic to pods that aren't ready.
- Integrate health checks with liveness/readiness using a dedicated `/health` endpoint.
- Add observability (metrics + logs) to tune HPA and resource limits.
