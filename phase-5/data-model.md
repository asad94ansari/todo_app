# Data Model: Phase V — GitHub Actions & CD

**Feature**: Phase V — GitHub Actions & CD
**Created**: 2026-02-08

## Entity Definitions

### Workflow Configuration Entity

**Description**: Represents the GitHub Actions workflow configuration

**Fields**:
- `name`: String (Required)
  - Purpose: Unique identifier for the workflow
  - Constraints: Must follow GitHub Actions naming conventions
  - Validation: Alphanumeric characters, spaces, hyphens; 1-100 characters

- `trigger`: Object (Required)
  - Purpose: Defines when the workflow runs
  - Constraints: Follows GitHub Actions trigger syntax
  - Validation: Must include 'push' to 'main' branch

- `jobs`: Array of Objects (Required)
  - Purpose: List of jobs to execute in the workflow
  - Constraints: Each job must have unique name and proper dependencies
  - Validation: Jobs must follow execution order (Lint → Build/Push → Update Manifests)

- `concurrency`: Object (Optional)
  - Purpose: Defines concurrency group to cancel previous runs
  - Constraints: Follows GitHub Actions concurrency syntax
  - Validation: Should cancel previous runs to prevent conflicts

- `permissions`: Object (Required)
  - Purpose: Defines permissions for the workflow
  - Constraints: Must include proper permissions for GHCR access
  - Validation: Must allow contents: read and packages: write

### Docker Image Entity

**Description**: Represents a Docker image built and pushed to GHCR

**Fields**:
- `id`: String (Primary Key)
  - Purpose: Unique identifier for the image
  - Constraints: Follows Docker image naming convention
  - Validation: Must include GHCR registry path

- `repository`: String (Required)
  - Purpose: Repository name in GHCR
  - Constraints: Must be valid GitHub repository name
  - Validation: Alphanumeric characters, hyphens, underscores

- `tag`: String (Required)
  - Purpose: Version tag for the image
  - Constraints: Short SHA or GitHub Run Number format
  - Validation: Should be unique for each build

- `service`: String (Required)
  - Purpose: Which service this image represents (backend, frontend, mcp-server)
  - Constraints: Must be one of the defined services
  - Validation: Must match one of the known service types

- `createdAt`: DateTime (Required)
  - Purpose: When the image was built
  - Constraints: Auto-generated on creation
  - Validation: System-generated timestamp in ISO format

### Helm Values Entity

**Description**: Represents the Helm values configuration for Kubernetes deployment

**Fields**:
- `id`: String (Primary Key)
  - Purpose: Unique identifier for the values configuration
  - Constraints: Must be unique per environment
  - Validation: Follows naming convention with environment suffix

- `environment`: String (Required)
  - Purpose: Target environment (staging, production, etc.)
  - Constraints: Must be one of predefined environments
  - Validation: Must be valid environment name

- `imageTags`: Object (Required)
  - Purpose: Map of service names to their image tags
  - Constraints: Must include tags for all services
  - Validation: Each tag must correspond to a valid image in GHCR

- `overrides`: Object (Optional)
  - Purpose: Additional configuration overrides for the environment
  - Constraints: Must be valid Helm value overrides
  - Validation: Should pass Helm linting

- `updatedAt`: DateTime (Required)
  - Purpose: When the values were last updated
  - Constraints: Auto-updated on modification
  - Validation: System-managed timestamp in ISO format

### Secret Configuration Entity

**Description**: Represents repository secrets used for secure deployment

**Fields**:
- `name`: String (Primary Key)
  - Purpose: Unique identifier for the secret
  - Constraints: Must be valid GitHub secret name
  - Validation: Uppercase alphanumeric with underscores

- `purpose`: String (Required)
  - Purpose: What the secret is used for
  - Constraints: Must describe the secret's use case
  - Validation: Should be clear and specific

- `requiredFor`: Array of Strings (Required)
  - Purpose: List of workflow steps that require this secret
  - Constraints: Must reference valid workflow steps
  - Validation: Should be actively used in the workflow

- `encrypted`: Boolean (Required)
  - Purpose: Whether the secret is encrypted
  - Constraints: Always true for repository secrets
  - Validation: Must be properly encrypted by GitHub

## Relationships

### Workflow Configuration to Docker Image
- **Relationship Type**: One-to-Many (One workflow builds many images)
- **Cardinality**: 1 Workflow → 0..* Docker Images
- **Constraint**: Workflow generates images based on service definitions
- **Cascade Behavior**: Images remain when workflow changes

### Docker Image to Helm Values
- **Relationship Type**: Many-to-One (Many images referenced by one values file)
- **Cardinality**: 0..* Docker Images → 1 Helm Values
- **Constraint**: Values file contains image tags for multiple services
- **Update Pattern**: Values updated when new images are available

### Secret Configuration to Workflow Configuration
- **Relationship Type**: Many-to-Many (Multiple secrets used by multiple workflows)
- **Cardinality**: 0..* Secrets → 0..* Workflows
- **Constraint**: Workflows reference secrets for secure operations
- **Access Pattern**: Secrets pulled as needed during workflow execution

## Validation Rules

### At Creation Time:
- Workflow must have valid trigger configuration for 'main' branch
- Docker image repository must follow GHCR naming convention
- Helm values must include all required service image tags
- Secrets must be properly encrypted and accessible

### At Update Time:
- Docker image tags must correspond to actual images in GHCR
- Helm values must pass validation before deployment
- Workflow job dependencies must be maintained
- Secret configurations should remain consistent

### Access Control:
- GitHub Actions workflows run with limited permissions
- GHCR access restricted to repository scope
- Secrets only accessible during workflow execution
- Image pulling restricted to authenticated access