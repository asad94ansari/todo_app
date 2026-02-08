# Research Document: Phase IV — K8s Local Deployment

**Feature**: Phase IV — K8s Local Deployment
**Created**: 2026-02-07

## Research Findings

### Decision: Resource Limits for Services
**Rationale**: For local development, we'll use conservative resource limits that ensure the application runs smoothly without consuming excessive resources. For local Minikube development, we'll set CPU and memory limits that are reasonable for a development environment.
**Alternatives considered**:
- High limits (2 CPU / 4GB RAM) - overkill for local development
- Conservative limits (0.5 CPU / 512MB RAM) - suitable for local development (selected approach)
- Default limits (1 CPU / 1GB RAM) - balanced approach
- No limits - not recommended for production-like testing

### Decision: Service Exposure Method
**Rationale**: For local Minikube development, NodePort is more reliable and easier to work with than LoadBalancer, which requires cloud provider support. NodePort allows consistent access to the frontend through a specific port.
**Alternatives considered**:
- LoadBalancer - requires cloud provider, not ideal for local Minikube
- NodePort (selected approach) - works reliably with Minikube, accessible via minikube service URL
- ClusterIP + Port Forwarding - requires additional manual steps
- Ingress Controller - adds complexity for local development

### Decision: Persistent Storage Approach
**Rationale**: For local development with Minikube, we'll use ephemeral storage (emptyDir volumes) which is appropriate for development. For production deployments, persistent volumes would be used, but for local development the database can be ephemeral.
**Alternatives considered**:
- Ephemeral storage with emptyDir (selected approach - suitable for local development)
- PersistentVolumes with hostPath - could work but ties data to specific nodes
- StatefulSets with PVCs - overkill for local development environment
- External database service - adds complexity for local development

### Decision: Image Optimization Strategy
**Rationale**: Multi-stage builds with specific lightweight base images (python:3.13-slim for backend, node:alpine for frontend) provide the best balance of image size reduction and functionality. Using build arguments and proper layer caching further optimizes the builds.
**Alternatives considered**:
- Single stage builds - results in larger images
- Multi-stage with slim/alpine bases (selected approach - smaller images, fewer packages)
- Distroless images - very small but requires more complex setup for Python apps
- Custom minimal images - too much complexity for this use case

### Decision: Health Probes Configuration
**Rationale**: Implementing both liveness and readiness probes with appropriate timeouts and intervals ensures that Kubernetes can properly manage pod lifecycles and traffic routing. Using simple HTTP endpoints for probe health checks.
**Alternatives considered**:
- No probes - not recommended for production-like environments
- TCP socket checks - less informative than HTTP checks
- HTTP GET probes (selected approach - provides application-level health info)
- Command execution checks - more overhead than HTTP checks

### Decision: Helm Chart Structure
**Rationale**: Organizing the Helm chart with a single umbrella chart that includes all services provides easy management while maintaining proper separation of concerns. Using standard Helm patterns with configurable values.
**Alternatives considered**:
- Single umbrella chart (selected approach - simple to deploy and manage)
- Separate charts for each service - more complex deployment process
- Monorepo approach with subcharts - good balance but adds complexity