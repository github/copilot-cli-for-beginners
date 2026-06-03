Kubernetes deployment for the Bookkeeper sample

This folder contains a `ConfigMap` with `data.json` and a `Job` manifest that runs the CLI command `python book_app.py list`.

Usage (build and push image to a registry first):

```bash
# Build and tag
cd samples/book-app-project
docker build -t ghcr.io/<your-user>/bookkeeper-app:latest .

# Push (example: GitHub Container Registry)
docker push ghcr.io/<your-user>/bookkeeper-app:latest

# Apply k8s resources
kubectl apply -f k8s/configmap-data.yaml
kubectl apply -f k8s/job-list.yaml

# Watch job
kubectl get jobs
kubectl logs job/bookkeeper-list-job
```

Notes:
- The sample app is a CLI, not a long-running server. A `Job` is used to execute a one-time command.
- If you use a local cluster (kind/minikube) you may need to load the local image into the cluster instead of pushing to a registry.
