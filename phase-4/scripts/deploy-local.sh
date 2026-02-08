#!/bin/bash

# Script to deploy the todo application stack to a local Minikube cluster

set -e  # Exit on any error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
HELM_CHART_DIR="$ROOT_DIR/helm-charts/todo-stack"

echo "🚀 Starting deployment of Todo Application Stack to Minikube..."

# Check if Minikube is running
if ! minikube status &>/dev/null; then
    echo "❌ Minikube is not running. Starting Minikube..."
    minikube start
else
    echo "✅ Minikube is already running"
fi

# Check if Helm is available
if ! command -v helm &>/dev/null; then
    echo "❌ Helm is not installed. Please install Helm first."
    exit 1
fi

# Build Docker images
echo "🐳 Building Docker images..."

# Backend image
echo "📦 Building backend image..."
docker build -f "$ROOT_DIR/docker/backend.Dockerfile" -t todo-backend:latest "$ROOT_DIR/../phase-2/backend"

# Frontend image
echo "📦 Building frontend image..."
docker build -f "$ROOT_DIR/docker/frontend.Dockerfile" -t todo-frontend:latest "$ROOT_DIR/../phase-2/frontend"

# MCP Server image
echo "📦 Building MCP server image..."
docker build -f "$ROOT_DIR/docker/mcp-server.Dockerfile" -t todo-mcp-server:latest "$ROOT_DIR/../phase-3/mcp-server"

# Load images into Minikube
echo "📥 Loading images into Minikube..."
minikube image load todo-backend:latest
minikube image load todo-frontend:latest
minikube image load todo-mcp-server:latest

# Navigate to Helm chart directory
cd "$HELM_CHART_DIR"

# Verify Helm chart
echo "🔍 Linting Helm chart..."
helm lint .

# Check if release already exists
if helm status todo-app &>/dev/null; then
    echo "🔄 Upgrading existing release..."
    helm upgrade todo-app .
else
    echo "_INSTALLING new release..."
    helm install todo-app .
fi

echo "⏳ Waiting for deployments to be ready..."

# Wait for deployments to be ready
kubectl wait --for=condition=ready pod -l app=todo-backend --timeout=180s
kubectl wait --for=condition=ready pod -l app=todo-frontend --timeout=180s
kubectl wait --for=condition=ready pod -l app=todo-mcp-server --timeout=180s

echo "✅ Deployments are ready!"

# Get service information
echo "📋 Service information:"
kubectl get services

# Provide access information
echo "🌐 Access information:"
FRONTEND_SVC=$(kubectl get service -l app=todo-frontend -o jsonpath='{.items[0].metadata.name}')
if [ ! -z "$FRONTEND_SVC" ]; then
    FRONTEND_URL=$(minikube service "$FRONTEND_SVC" --url)
    echo "Frontend URL: $FRONTEND_URL"
fi

echo "💡 To access the application, you can also run: minikube tunnel"
echo "💡 To check logs: kubectl logs -l app=todo-backend (or todo-frontend, todo-mcp-server)"
echo "🎉 Deployment completed successfully!"