# Phase V - GitHub Actions & CD

This is the implementation of the Phase V CI/CD pipeline using GitHub Actions. It automates the building, testing, and deployment of the todo application services to a Kubernetes cluster using GitHub Container Registry (GHCR) and Helm.

## Features

- Automated CI/CD pipeline triggered on pushes to the 'main' branch
- Multi-job workflow with linting, building/pushing, and manifest updating
- Docker image building for Backend, Frontend, and MCP Server services
- Image tagging with GitHub commit SHA for traceability
- Pushing to GitHub Container Registry (GHCR)
- Helm-based deployment manifest updates
- Code quality checks with Python (ruff/flake8) and Next.js (eslint)
- Simulated deployment to Kubernetes cluster

## Architecture

The CI/CD pipeline follows a cloud-native approach:

- **Trigger**: GitHub Actions workflow triggered on push to 'main' branch
- **Linting Job**: Code quality checks for Python and JavaScript code
- **Build & Push Job**: Docker image building with Buildx and pushing to GHCR
- **Update Manifests Job**: Helm values updates with new image tags
- **Deployment Simulation**: Validation of Kubernetes manifests without actual deployment
- **Security**: Proper authentication using GITHUB_TOKEN and repository secrets

## Files Structure

```
phase-5/
├── .github/
│   └── workflows/
│       └── deploy.yml              # Main CI/CD workflow
├── scripts/
│   └── update-tags.sh              # Script to update image tags in Helm values
├── plan.md                         # Implementation plan
├── research.md                     # Research and decisions
├── data-model.md                   # Data models for CI/CD entities
├── contracts/
│   └── api-contracts.md            # API contracts for workflow interfaces
├── quickstart.md                   # Quickstart guide
└── README.md                       # This file
```

## Workflow Configuration

### Jobs

1. **Lint**: Runs code quality checks (Python ruff/flake8, JS/TS eslint)
2. **Build & Push**: Builds Docker images and pushes to GHCR with commit SHA tags
3. **Update Manifests**: Updates Helm values with new image tags
4. **Deploy Simulation**: Validates Kubernetes manifests without actual deployment

### Triggers

- Push to 'main' branch
- Pull requests to 'main' branch (read-only operations)

### Concurrency

- Cancels previous runs to prevent conflicts when new commits are pushed

## Configuration

### Repository Secrets

Required secrets for the workflow (add in Settings → Secrets and Variables → Actions):

- `GITHUB_TOKEN`: Automatically provided by GitHub Actions (for GHCR access)
- `KUBECONFIG`: Kubernetes cluster access configuration (for real deployment)

### Image Tagging

Docker images are tagged with:
- Commit SHA for traceability (e.g., `sha-abc123d`)
- Latest tag for default deployment
- Date-prefixed short SHA (e.g., `20260208-abc123d`)

## Running the Pipeline

The pipeline runs automatically when code is pushed to the 'main' branch. You can also manually trigger it from the GitHub Actions tab in your repository.

### Verification

1. Check that all jobs complete successfully in the Actions tab
2. Verify Docker images are pushed to GHCR with correct tags
3. Confirm Helm values are updated with new image tags
4. Review generated Kubernetes manifests in the workflow logs

## Customization

### Environment Configuration

The workflow supports different environments through variables in the workflow file. Update the `deploy.yml` file to customize for staging/production environments.

### Additional Checks

You can add more quality checks by extending the lint job in the workflow file.

## Troubleshooting

### Workflow Fails During Linting
- Check that Python code follows Ruff/flake8 standards
- Verify that JavaScript code follows ESLint standards
- Look at the specific error messages in the workflow logs

### Docker Build Fails
- Verify that Dockerfiles exist in the expected locations
- Check that Docker images can be built locally before pushing

### Image Push Fails
- Verify that GITHUB_TOKEN has proper permissions for GHCR
- Check that repository name follows GHCR naming conventions

### Helm Update Fails
- Verify that Helm chart files exist and are valid
- Check that yq tool is available in the CI environment