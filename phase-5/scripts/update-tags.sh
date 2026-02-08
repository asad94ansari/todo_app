#!/bin/bash

# Script to update image tags in Helm values.yaml
# Usage: ./update-tags.sh <commit-sha>

set -e  # Exit on any error

if [ $# -eq 0 ]; then
    echo "Usage: $0 <commit-sha>"
    exit 1
fi

COMMIT_SHA=$1
HELM_VALUES_PATH="phase-4/helm-charts/todo-stack/values.yaml"

echo "Updating image tags in Helm values with SHA: $COMMIT_SHA"

# Check if values.yaml exists
if [ ! -f "$HELM_VALUES_PATH" ]; then
    echo "Error: Helm values file not found at $HELM_VALUES_PATH"
    exit 1
fi

# Update image tags using yq
if command -v yq &> /dev/null; then
    # Update backend image tag
    yq eval ".backend.image.tag = \"$COMMIT_SHA\"" -i "$HELM_VALUES_PATH"
    echo "Updated backend image tag to $COMMIT_SHA"

    # Update frontend image tag
    yq eval ".frontend.image.tag = \"$COMMIT_SHA\"" -i "$HELM_VALUES_PATH"
    echo "Updated frontend image tag to $COMMIT_SHA"

    # Update MCP server image tag
    yq eval ".mcpServer.image.tag = \"$COMMIT_SHA\"" -i "$HELM_VALUES_PATH"
    echo "Updated MCP server image tag to $COMMIT_SHA"
else
    echo "Error: yq is not installed. Please install yq to update Helm values."
    exit 1
fi

echo "Image tags updated successfully in $HELM_VALUES_PATH"