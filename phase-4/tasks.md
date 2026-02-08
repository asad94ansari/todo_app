# Tasks: Phase IV — K8s Local Deployment

**Feature**: Phase IV — K8s Local Deployment
**Generated**: 2026-02-07
**Status**: Draft

## Dependencies

- User Story 1 (P1) - Local Kubernetes Deployment (Foundation for all other stories)
- User Story 2 (P1) - Containerized Services (Depends on foundational setup)
- User Story 3 (P2) - Automated Deployment Management (Depends on User Story 1 & 2)

## Implementation Strategy

Build MVP with containerization first (User Story 2), then extend with orchestration (User Story 1), followed by automated deployment (User Story 3). This ensures all services are properly containerized before working on orchestration.

## Phase 1: Setup

- [X] T001 Create project structure with docker, helm-charts, and scripts directories
- [X] T002 Set up Docker environment for multi-stage builds
- [X] T003 Set up Helm chart directory structure

## Phase 2: Foundational Tasks

- [X] T004 Configure Docker build environment with multi-stage capabilities
- [X] T005 Initialize Helm chart structure in phase-4/helm-charts/todo-stack/
- [X] T006 Set up deployment scripts directory

## Phase 3: User Story 2 - Containerized Services (P1)

**Goal**: Create optimized Docker images for all three services

**Independent Test Criteria**:
- Each service builds into an optimized Docker image
- Images follow multi-stage build pattern with minimal base images
- Containerized services maintain all functionality

**Tasks**:

- [X] T007 [P] [US2] Create multi-stage Dockerfile for FastAPI Backend in phase-4/docker/backend.Dockerfile
- [X] T008 [P] [US2] Create multi-stage Dockerfile for Next.js Frontend in phase-4/docker/frontend.Dockerfile
- [X] T009 [US2] Create Dockerfile for MCP Server in phase-4/docker/mcp-server.Dockerfile
- [X] T010 [US2] Test backend image builds successfully with python-slim base
- [X] T011 [US2] Test frontend image builds successfully with node-alpine base
- [X] T012 [US2] Test MCP server image builds successfully with python-slim base

## Phase 4: User Story 1 - Local Kubernetes Deployment (P1)

**Goal**: Deploy containerized services to local Kubernetes cluster with proper networking

**Independent Test Criteria**:
- All services deploy to Minikube cluster successfully
- Services communicate with each other via internal DNS
- Frontend is accessible externally via NodePort/LoadBalancer

**Tasks**:

- [X] T013 [P] [US1] Create Kubernetes Deployment for Backend in phase-4/helm-charts/todo-stack/templates/deployment-backend.yaml
- [X] T014 [P] [US1] Create Kubernetes Deployment for Frontend in phase-4/helm-charts/todo-stack/templates/deployment-frontend.yaml
- [X] T015 [US1] Create Kubernetes Deployment for MCP Server in phase-4/helm-charts/todo-stack/templates/deployment-mcp-server.yaml
- [X] T016 [US1] Create Kubernetes Service for Backend in phase-4/helm-charts/todo-stack/templates/service-backend.yaml
- [X] T017 [P] [US1] Create Kubernetes Service for Frontend in phase-4/helm-charts/todo-stack/templates/service-frontend.yaml
- [X] T018 [US1] Create Kubernetes Service for MCP Server in phase-4/helm-charts/todo-stack/templates/service-mcp-server.yaml
- [X] T019 [US1] Create ConfigMap for non-sensitive settings in phase-4/helm-charts/todo-stack/templates/configmap-backend.yaml
- [X] T020 [US1] Implement Helm values configuration for environment variables
- [X] T021 [US1] Test service-to-service communication works within cluster

## Phase 5: User Story 3 - Automated Deployment Management (P2)

**Goal**: Automate the deployment process with Helm and helper scripts

**Independent Test Criteria**:
- Entire stack deploys with single Helm command
- Deployment script builds images and installs Helm chart
- Environment variables and secrets configured properly

**Tasks**:

- [X] T022 [P] [US3] Configure values.yaml for secrets and environment variables
- [X] T023 [US3] Create deployment script deploy-local.sh in phase-4/scripts/deploy-local.sh
- [X] T024 [US3] Implement proper resource configuration in Helm templates
- [X] T025 [US3] Add liveness and readiness probes to deployments
- [X] T026 [US3] Test complete Helm chart installation with all services

## Phase 6: Integration and Testing

- [X] T027 Verify all pods reach 'Running' state in local cluster
- [X] T028 Test that frontend is reachable via minikube service command
- [X] T029 Verify inter-service communication works correctly
- [X] T030 Test complete deployment with all three services functional
- [X] T031 Validate all Phase 3 AI Chatbot functionality works within cluster
- [X] T032 Run end-to-end integration tests
- [X] T033 Verify deployment is reproducible across different environments

## Phase 7: Polish and Validation

- [X] T034 Add error handling and logging to deployment scripts
- [X] T035 Add health checks and monitoring configurations
- [X] T036 Update documentation and README files
- [X] T037 Final validation of all acceptance criteria
- [X] T038 Optimize resource usage for local development environment
- [X] T039 Verify single 'helm install' deploys entire stack successfully

## Parallel Execution Opportunities

- Dockerfiles for all services can be developed in parallel (T007, T008, T009)
- Kubernetes deployments can be created in parallel (T013, T014, T015)
- Kubernetes services can be created in parallel (T016, T017, T018)
- Testing tasks can be executed in parallel with implementation (T027-T033)