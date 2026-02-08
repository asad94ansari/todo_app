# Quickstart Guide: Phase IV — K8s Local Deployment

**Feature**: Phase IV — K8s Local Deployment
**Created**: 2026-02-07

## Overview
This guide explains how to set up and run the todo application stack on a local Kubernetes cluster using Minikube and Helm.

## Prerequisites
- Docker (for building images)
- Minikube (local Kubernetes cluster)
- Helm (package manager for Kubernetes)
- kubectl (Kubernetes command-line tool)
- git (for cloning repositories)

## Project Structure
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
│       │   ├── deployment-backend.yaml
│       │   ├── deployment-frontend.yaml
│       │   ├── deployment-mcp.yaml
│       │   ├── service-backend.yaml
│       │   ├── service-frontend.yaml
│       │   ├── service-mcp.yaml
│       │   ├── configmap-backend.yaml
│       │   └── secret-backend.yaml
└── scripts/
    └── deploy-local.sh
```

## Setting Up Minikube

### 1. Start Minikube
```bash
minikube start
```

### 2. Verify Minikube is running
```bash
minikube status
kubectl cluster-info
```

## Building Docker Images

### 1. Navigate to the docker directory
```bash
cd phase-4/docker
```

### 2. Build the backend image
```bash
docker build -f backend.Dockerfile -t todo-backend:latest ../../phase-2/backend
```

### 3. Build the frontend image
```bash
docker build -f frontend.Dockerfile -t todo-frontend:latest ../../phase-2/frontend
```

### 4. Build the MCP server image
```bash
docker build -f mcp-server.Dockerfile -t todo-mcp-server:latest ../../phase-3/mcp-server
```

### 5. Load images into Minikube
```bash
minikube image load todo-backend:latest
minikube image load todo-frontend:latest
minikube image load todo-mcp-server:latest
```

## Installing the Helm Chart

### 1. Navigate to the helm-charts directory
```bash
cd ../helm-charts/todo-stack
```

### 2. Verify the chart
```bash
helm lint .
```

### 3. Install the chart with default values
```bash
helm install todo-app .
```

### 4. Install the chart with custom values (if needed)
```bash
helm install todo-app . --values custom-values.yaml
```

## Accessing the Application

### 1. Check that all pods are running
```bash
kubectl get pods
```

### 2. Check the services
```bash
kubectl get services
```

### 3. Access the frontend via NodePort
```bash
minikube service todo-app-frontend --url
```

### 4. Alternatively, access the frontend via tunnel
```bash
minikube tunnel
```
Then access the frontend using the NodePort shown in `kubectl get services`.

## Customizing Configuration

### 1. Create a custom values file
```bash
cp values.yaml custom-values.yaml
```

### 2. Edit custom-values.yaml to configure:
- Database connection URLs
- API keys
- Resource limits
- Replicas count
- Service types

### 3. Install with custom values
```bash
helm install todo-app . --values custom-values.yaml
```

## Upgrading the Deployment

### 1. Update the chart or values
```bash
helm upgrade todo-app . --values custom-values.yaml
```

## Uninstalling the Application

### Remove the Helm release
```bash
helm uninstall todo-app
```

## Useful Commands

### View logs
```bash
kubectl logs -l app=todo-backend
kubectl logs -l app=todo-frontend
kubectl logs -l app=todo-mcp-server
```

### Port forward for debugging
```bash
kubectl port-forward svc/todo-app-backend 8000:8000
kubectl port-forward svc/todo-app-frontend 3000:3000
kubectl port-forward svc/todo-app-mcp 8080:8080
```

### Get status
```bash
helm status todo-app
```

## Troubleshooting

### Pods stuck in 'Pending' status
- Check resource limits in values.yaml
- Ensure Minikube has sufficient resources allocated

### Services not accessible
- Verify service type (NodePort vs LoadBalancer)
- Check Minikube is running with proper tunnel access

### Images not found
- Ensure images are loaded into Minikube
- Check image tags match what's specified in values.yaml