# Quickstart Guide: Phase V — GitHub Actions & CD

**Feature**: Phase V — GitHub Actions & CD
**Created**: 2026-02-08

## Overview
This guide explains how to set up and run the GitHub Actions CI/CD pipeline for the todo application, automating the build, push, and deployment process to Kubernetes.

## Prerequisites
- GitHub repository with the todo application code
- GitHub Container Registry (GHCR) access
- Kubernetes cluster access (for real deployment)
- Repository secrets configured for sensitive data
- Docker, Helm, and yq tools available in the CI environment

## Repository Setup

### 1. Enable GitHub Container Registry
The workflow will push Docker images to GHCR. Ensure your repository has package publishing enabled.

### 2. Configure Repository Secrets
Add the following secrets to your repository (Settings → Secrets and Variables → Actions):

- `OPENAI_API_KEY`: API key for AI features (if needed)
- `DATABASE_URL`: Database connection string (if needed)
- `KUBECONFIG`: Kubernetes cluster access configuration (for real deployment)

## Workflow Structure

### 1. File Locations
```
.github/
└── workflows/
    └── deploy.yml           # Main CI/CD workflow
phase-5/
└── scripts/
    └── update-tags.sh       # Script to update image tags in Helm values
```

### 2. Workflow Configuration
The main workflow consists of three jobs:
- `lint`: Runs code quality checks
- `build-and-push`: Builds Docker images and pushes to GHCR
- `update-manifests`: Updates Helm values with new image tags

## Setting Up the Workflow

### 1. Create the GitHub Actions workflow
The workflow file `.github/workflows/deploy.yml` will be created with the following components:

1. **Trigger**: On push to 'main' branch
2. **Concurrency**: Cancel previous runs to prevent conflicts
3. **Jobs**: Lint → Build/Push → Update Manifests sequence
4. **Permissions**: Contents read and packages write for GHCR

### 2. Configure Docker Images
The workflow will build Docker images for:
- Backend service (FastAPI)
- Frontend service (Next.js)
- MCP Server service

Images will be tagged with short SHA for traceability.

### 3. Set Up Helm Integration
The workflow will update Helm values with new image tags and generate updated manifests.

## Running the Workflow

### 1. Push Code to Main Branch
The workflow automatically triggers when you push to the 'main' branch:
```bash
git add .
git commit -m "Update application code"
git push origin main
```

### 2. Monitor Workflow Execution
Check the Actions tab in your GitHub repository to monitor the workflow execution.

### 3. Verify Image Builds
After successful execution, verify that images are pushed to GHCR:
- Navigate to the "Packages" section in your repository
- Confirm that new images with SHA tags are available

## Customizing the Workflow

### 1. Environment Configuration
The workflow supports different environments (staging/production) through environment variables in the workflow file.

### 2. Image Tagging Strategy
By default, images are tagged with short SHA. You can modify this in the workflow to use other strategies like GitHub run numbers.

### 3. Deployment Simulation
The workflow includes a deployment simulation step that validates manifests without actually deploying to a live cluster.

## Troubleshooting

### Workflow Fails During Linting
- Check that Python code follows Ruff/flake8 standards
- Verify that JavaScript code follows ESLint standards
- Look at the specific error messages in the workflow logs

### Docker Build Fails
- Verify that Dockerfiles exist in the expected locations
- Check that Docker images can be built locally before pushing
- Ensure proper base images are used for multi-stage builds

### Image Push Fails
- Verify that GITHUB_TOKEN has proper permissions for GHCR
- Check that repository name follows GHCR naming conventions
- Confirm that image tagging strategy is correctly implemented

### Helm Update Fails
- Verify that Helm chart files exist and are valid
- Check that yq tool is available in the CI environment
- Ensure proper Helm values file paths are specified