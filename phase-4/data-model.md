# Data Model: Phase IV — K8s Local Deployment

**Feature**: Phase IV — K8s Local Deployment
**Created**: 2026-02-07

## Entity Definitions

### K8sDeployment Entity

**Description**: Represents a Kubernetes Deployment configuration for a service

**Fields**:
- `name`: String (Required)
  - Purpose: Unique identifier for the deployment
  - Constraints: Must follow DNS-1123 subdomain naming convention
  - Validation: Alphanumeric characters, hyphens, dots; 1-253 characters

- `image`: String (Required)
  - Purpose: Docker image reference with tag
  - Constraints: Valid Docker image reference format
  - Validation: Must include registry, repository, and tag

- `replicas`: Integer (Optional)
  - Purpose: Number of pod replicas to maintain
  - Constraints: Non-negative integer
  - Validation: Default to 1 if not specified

- `resources`: Object (Optional)
  - Purpose: CPU and memory resource requests and limits
  - Constraints: Kubernetes resource requirements format
  - Validation: Must specify both requests and limits for production readiness

- `ports`: Array of Objects (Required)
  - Purpose: Container port mappings
  - Constraints: Each object must have containerPort and optional name
  - Validation: containerPort must be valid port number (1-65535)

- `env`: Array of Objects (Optional)
  - Purpose: Environment variables for the container
  - Constraints: Each object must have name and either value or valueFrom
  - Validation: Names must be valid environment variable names

- `livenessProbe`: Object (Optional)
  - Purpose: Health check configuration for liveness
  - Constraints: Follows Kubernetes probe specification
  - Validation: Must specify either HTTP, TCP, or command probe

- `readinessProbe`: Object (Optional)
  - Purpose: Health check configuration for readiness
  - Constraints: Follows Kubernetes probe specification
  - Validation: Must specify either HTTP, TCP, or command probe

### K8sService Entity

**Description**: Represents a Kubernetes Service configuration for network access

**Fields**:
- `name`: String (Required)
  - Purpose: Unique identifier for the service
  - Constraints: Must follow DNS-1123 subdomain naming convention
  - Validation: Alphanumeric characters, hyphens, dots; 1-253 characters

- `type`: String (Required)
  - Purpose: Service type (ClusterIP, NodePort, LoadBalancer, ExternalName)
  - Constraints: Must be one of the valid Kubernetes service types
  - Validation: Default to ClusterIP for internal services

- `selector`: Object (Required)
  - Purpose: Label selector for pod association
  - Constraints: Key-value pairs matching deployment labels
  - Validation: Must match deployment's label selectors

- `ports`: Array of Objects (Required)
  - Purpose: Port mappings for the service
  - Constraints: Each object must have port and targetPort
  - Validation: Port numbers must be valid (1-65535)

- `clusterIP`: String (Optional)
  - Purpose: IP address for the service
  - Constraints: Valid IP address format
  - Validation: Generally left empty for dynamic assignment

### ConfigMap Entity

**Description**: Represents Kubernetes ConfigMap for configuration data

**Fields**:
- `name`: String (Required)
  - Purpose: Unique identifier for the ConfigMap
  - Constraints: Must follow DNS-1123 subdomain naming convention
  - Validation: Alphanumeric characters, hyphens, dots; 1-253 characters

- `data`: Object (Required)
  - Purpose: Key-value pairs of configuration data
  - Constraints: Values must be strings
  - Validation: Keys must be valid identifiers

- `binaryData`: Object (Optional)
  - Purpose: Binary data encoded as base64
  - Constraints: Base64-encoded values
  - Validation: Values must be properly base64-encoded

### Secret Entity

**Description**: Represents Kubernetes Secret for sensitive data

**Fields**:
- `name`: String (Required)
  - Purpose: Unique identifier for the Secret
  - Constraints: Must follow DNS-1123 subdomain naming convention
  - Validation: Alphanumeric characters, hyphens, dots; 1-253 characters

- `data`: Object (Optional)
  - Purpose: Base64-encoded key-value pairs of sensitive data
  - Constraints: Base64-encoded values
  - Validation: Values must be properly base64-encoded

- `stringData`: Object (Optional)
  - Purpose: Unencoded key-value pairs of sensitive data (encoded automatically)
  - Constraints: Values are automatically base64-encoded
  - Validation: Values will be encoded before storage

## Relationships

### K8sDeployment to K8sService
- **Relationship Type**: One-to-Many (One deployment can be accessed by multiple services)
- **Cardinality**: 1 Deployment → 0..* Services
- **Constraint**: Service selector must match deployment labels
- **Communication Pattern**: Services route traffic to deployment pods

### K8sDeployment to ConfigMap
- **Relationship Type**: Many-to-Many (Multiple deployments can use multiple ConfigMaps)
- **Cardinality**: 0..* Deployments → 0..* ConfigMaps
- **Constraint**: ConfigMaps mounted as volumes or referenced as environment variables
- **Usage Pattern**: Configuration data injected into pods

### K8sDeployment to Secret
- **Relationship Type**: Many-to-Many (Multiple deployments can use multiple Secrets)
- **Cardinality**: 0..* Deployments → 0..* Secrets
- **Constraint**: Secrets mounted as volumes or referenced as environment variables
- **Usage Pattern**: Sensitive configuration injected into pods

## Validation Rules

### At Creation Time:
- Deployment name must be unique within namespace
- Service selector must match an existing deployment's labels
- Image reference must be valid
- Port numbers must be in valid range (1-65535)
- Environment variable names must be valid identifiers

### At Update Time:
- Replica count can be adjusted safely
- Resource requests/limits can be modified
- Environment variables can be added/removed
- Service type changes may require recreation

### Access Control:
- Secrets and ConfigMaps must be in same namespace as deployment
- RBAC may be required for cross-namespace references
- Service accounts may be required for specific operations