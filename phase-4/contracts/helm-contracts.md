# Helm Chart Contracts: Phase IV — K8s Local Deployment

**Feature**: Phase IV — K8s Local Deployment
**Contract Version**: 1.0
**Created**: 2026-02-07

## Purpose
Defines the Helm chart interface contracts for the todo application stack deployment.

## Helm Chart Interface

### Chart Metadata
- **Name**: `todo-stack`
- **Version**: Chart version follows semantic versioning (e.g., 1.0.0)
- **AppVersion**: Application version (matches feature release version)
- **Description**: "Todo application stack with backend, frontend, and MCP server"
- **Keywords**: `["todo", "application", "fullstack", "ai-chatbot"]`
- **Home**: URL to documentation
- **Sources**: URLs to source repositories
- **Maintainers**: Contact information for maintainers

## Configuration Parameters

### Global Parameters
- **Parameter**: `global.imageRegistry`
  - **Description**: Global image registry to use for all images
  - **Type**: String
  - **Default**: `""` (empty - uses default)
  - **Constraints**: Valid registry URL format

- **Parameter**: `global.storageClass`
  - **Description**: Global storage class to use for persistent storage
  - **Type**: String
  - **Default**: `""` (uses default storage class)
  - **Constraints**: Valid storage class name in cluster

- **Parameter**: `global.imagePullSecrets`
  - **Description**: Global Docker registry authentication secrets
  - **Type**: Array of Strings
  - **Default**: `[]` (empty array)
  - **Constraints**: Valid secret names in cluster

### Backend Service Parameters
- **Parameter**: `backend.enabled`
  - **Description**: Whether to deploy the backend service
  - **Type**: Boolean
  - **Default**: `true`
  - **Constraints**: N/A

- **Parameter**: `backend.image.repository`
  - **Description**: Backend Docker image repository
  - **Type**: String
  - **Default**: `"todo-backend"`
  - **Constraints**: Valid Docker image repository name

- **Parameter**: `backend.image.tag`
  - **Description**: Backend Docker image tag
  - **Type**: String
  - **Default**: `""` (defaults to AppVersion)
  - **Constraints**: Valid Docker image tag

- **Parameter**: `backend.image.pullPolicy`
  - **Description**: Backend image pull policy
  - **Type**: String
  - **Default**: `"IfNotPresent"`
  - **Constraints**: Must be "Always", "Never", or "IfNotPresent"

- **Parameter**: `backend.replicaCount`
  - **Description**: Number of backend replicas
  - **Type**: Integer
  - **Default**: `1`
  - **Constraints**: Non-negative integer

- **Parameter**: `backend.service.type`
  - **Description**: Backend service type
  - **Type**: String
  - **Default**: `"ClusterIP"`
  - **Constraints**: Must be "ClusterIP", "NodePort", "LoadBalancer", or "ExternalName"

- **Parameter**: `backend.service.port`
  - **Description**: Backend service port
  - **Type**: Integer
  - **Default**: `8000`
  - **Constraints**: Valid port number (1-65535)

- **Parameter**: `backend.resources`
  - **Description**: Backend resource requests and limits
  - **Type**: Object
  - **Default**:
    ```yaml
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 500m
      memory: 512Mi
    ```
  - **Constraints**: Follows Kubernetes resource requirements format

### Frontend Service Parameters
- **Parameter**: `frontend.enabled`
  - **Description**: Whether to deploy the frontend service
  - **Type**: Boolean
  - **Default**: `true`
  - **Constraints**: N/A

- **Parameter**: `frontend.image.repository`
  - **Description**: Frontend Docker image repository
  - **Type**: String
  - **Default**: `"todo-frontend"`
  - **Constraints**: Valid Docker image repository name

- **Parameter**: `frontend.image.tag`
  - **Description**: Frontend Docker image tag
  - **Type**: String
  - **Default**: `""` (defaults to AppVersion)
  - **Constraints**: Valid Docker image tag

- **Parameter**: `frontend.replicaCount`
  - **Description**: Number of frontend replicas
  - **Type**: Integer
  - **Default**: `1`
  - **Constraints**: Non-negative integer

- **Parameter**: `frontend.service.type`
  - **Description**: Frontend service type
  - **Type**: String
  - **Default**: `"NodePort"` (for local access via Minikube)
  - **Constraints**: Must be "ClusterIP", "NodePort", "LoadBalancer", or "ExternalName"

- **Parameter**: `frontend.service.port`
  - **Description**: Frontend service port
  - **Type**: Integer
  - **Default**: `3000`
  - **Constraints**: Valid port number (1-65535)

- **Parameter**: `frontend.service.nodePort`
  - **Description**: NodePort for frontend access (when service.type is NodePort)
  - **Type**: Integer
  - **Default**: `""` (assigned automatically)
  - **Constraints**: Valid NodePort range (30000-32767) if specified

- **Parameter**: `frontend.resources`
  - **Description**: Frontend resource requests and limits
  - **Type**: Object
  - **Default**:
    ```yaml
    requests:
      cpu: 50m
      memory: 64Mi
    limits:
      cpu: 200m
      memory: 256Mi
    ```
  - **Constraints**: Follows Kubernetes resource requirements format

### MCP Server Parameters
- **Parameter**: `mcpServer.enabled`
  - **Description**: Whether to deploy the MCP server
  - **Type**: Boolean
  - **Default**: `true`
  - **Constraints**: N/A

- **Parameter**: `mcpServer.image.repository`
  - **Description**: MCP Server Docker image repository
  - **Type**: String
  - **Default**: `"todo-mcp-server"`
  - **Constraints**: Valid Docker image repository name

- **Parameter**: `mcpServer.image.tag`
  - **Description**: MCP Server Docker image tag
  - **Type**: String
  - **Default**: `""` (defaults to AppVersion)
  - **Constraints**: Valid Docker image tag

- **Parameter**: `mcpServer.replicaCount`
  - **Description**: Number of MCP server replicas
  - **Type**: Integer
  - **Default**: `1`
  - **Constraints**: Non-negative integer

- **Parameter**: `mcpServer.service.type`
  - **Description**: MCP Server service type
  - **Type**: String
  - **Default**: `"ClusterIP"`
  - **Constraints**: Must be "ClusterIP", "NodePort", "LoadBalancer", or "ExternalName"

- **Parameter**: `mcpServer.service.port`
  - **Description**: MCP Server service port
  - **Type**: Integer
  - **Default**: `8080`
  - **Constraints**: Valid port number (1-65535)

- **Parameter**: `mcpServer.resources`
  - **Description**: MCP Server resource requests and limits
  - **Type**: Object
  - **Default**:
    ```yaml
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 500m
      memory: 512Mi
    ```
  - **Constraints**: Follows Kubernetes resource requirements format

### Database Parameters (for backend)
- **Parameter**: `backend.database.url`
  - **Description**: Database connection URL
  - **Type**: String
  - **Default**: `""` (empty, requires configuration)
  - **Constraints**: Valid database URL format

- **Parameter**: `backend.database.host`
  - **Description**: Database host
  - **Type**: String
  - **Default**: `""` (empty)
  - **Constraints**: Valid hostname or IP address

- **Parameter**: `backend.database.port`
  - **Description**: Database port
  - **Type**: Integer
  - **Default**: `5432`
  - **Constraints**: Valid port number (1-65535)

### API Keys and Configuration
- **Parameter**: `backend.openai.apiKey`
  - **Description**: OpenAI API key for AI features
  - **Type**: String
  - **Default**: `""` (empty, requires configuration)
  - **Constraints**: Should be set via secret

- **Parameter**: `backend.jwt.secretKey`
  - **Description**: JWT secret key for authentication
  - **Type**: String
  - **Default**: `""` (empty, requires configuration)
  - **Constraints**: Should be strong, random secret

### Probes Configuration
- **Parameter**: `backend.livenessProbe.enabled`
  - **Description**: Enable liveness probe for backend
  - **Type**: Boolean
  - **Default**: `true`
  - **Constraints**: N/A

- **Parameter**: `backend.readinessProbe.enabled`
  - **Description**: Enable readiness probe for backend
  - **Type**: Boolean
  - **Default**: `true`
  - **Constraints**: N/A

- **Parameter**: `frontend.livenessProbe.enabled`
  - **Description**: Enable liveness probe for frontend
  - **Type**: Boolean
  - **Default**: `false` (typically not needed for static content)
  - **Constraints**: N/A

- **Parameter**: `mcpServer.livenessProbe.enabled`
  - **Description**: Enable liveness probe for MCP server
  - **Type**: Boolean
  - **Default**: `true`
  - **Constraints**: N/A

## Installation Interface

### Helm Install Command
```bash
helm install [RELEASE_NAME] . --values values.yaml
```

### Upgrade Command
```bash
helm upgrade [RELEASE_NAME] . --values values.yaml
```

### Uninstall Command
```bash
helm uninstall [RELEASE_NAME]
```

## Validation Rules
- All service ports must be valid (1-65535)
- Replica counts must be non-negative
- Image pull policies must be valid
- Resource requests must not exceed limits
- NodePort values must be in range 30000-32767 when specified
- Secret values should not be stored in values.yaml directly