# Phase IV - K8s Local Deployment

This is the implementation of the Phase IV Kubernetes local deployment for the todo application. It provides containerized deployments of the backend, frontend, and MCP server with Helm chart orchestration.

## Features

- Containerized services (Backend, Frontend, MCP Server) with optimized multi-stage Dockerfiles
- Helm chart for unified deployment management
- Kubernetes-native deployments, services, and configurations
- Proper service discovery and inter-service communication
- Resource configuration through values.yaml
- Liveness and readiness probes for all services
- Minikube-based local cluster environment

## Architecture

The application follows a cloud-native architecture pattern:

- **Containerization**: Multi-stage Docker builds with optimized base images
- **Orchestration**: Helm chart for unified deployment management
- **Networking**: Internal DNS-based communication between services
- **Configuration**: ConfigMaps and Secrets for environment variables
- **Monitoring**: Liveness and readiness probes for all deployments
- **Local Environment**: Minikube cluster for development and testing

## Files Structure

```
phase-4/
├── docker/
│   ├── backend.Dockerfile
│   ├── frontend.Dockerfile
│   └── mcp-server.Dockerfile
├── helm-charts/
│   └── todo-stack/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── templates/
│       │   ├── _helpers.tpl
│       │   ├── deployment-backend.yaml
│       │   ├── deployment-frontend.yaml
│       │   ├── deployment-mcp-server.yaml
│       │   ├── service-backend.yaml
│       │   ├── service-frontend.yaml
│       │   └── service-mcp-server.yaml
│       └── ...
├── scripts/
│   └── deploy-local.sh
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── README.md
```

## Prerequisites

- Docker
- Minikube
- Helm
- kubectl
- git

## Running the Application

### Automated Deployment

1. Make sure Minikube is running:
```bash
minikube start
```

2. Run the automated deployment script:
```bash
./phase-4/scripts/deploy-local.sh
```

The script will build all Docker images, load them into Minikube, and deploy the entire stack using Helm.

### Manual Deployment

1. Start Minikube:
```bash
minikube start
```

2. Build and load Docker images:
```bash
cd phase-4/docker
docker build -f backend.Dockerfile -t todo-backend:latest ../../phase-2/backend
docker build -f frontend.Dockerfile -t todo-frontend:latest ../../phase-2/frontend
docker build -f mcp-server.Dockerfile -t todo-mcp-server:latest ../../phase-3/mcp-server

minikube image load todo-backend:latest
minikube image load todo-frontend:latest
minikube image load todo-mcp-server:latest
```

3. Install the Helm chart:
```bash
cd ../helm-charts/todo-stack
helm install todo-app .
```

### Accessing the Application

1. Check that all pods are running:
```bash
kubectl get pods
```

2. Access the frontend via NodePort:
```bash
minikube service todo-stack-frontend-service --url
```

Alternatively, use:
```bash
minikube tunnel
```
Then access the frontend using the NodePort shown in `kubectl get services`.

## Configuration

Customize the deployment using the `values.yaml` file in the Helm chart directory. You can override values by creating a custom values file and installing with:
```bash
helm install todo-app . --values custom-values.yaml
```

## Helm Chart Parameters

See the `values.yaml` file for all configurable parameters, including:
- Image repositories and tags
- Replica counts
- Resource limits and requests
- Service types and ports
- Environment variables
- Probe configurations