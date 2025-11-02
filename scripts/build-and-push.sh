#!/bin/bash
# Build and push Docker image to Azure Container Registry

set -e

# Configuration
ACR_NAME="${ACR_NAME:-}"
IMAGE_NAME="medical-analyzer"
IMAGE_TAG="${IMAGE_TAG:-latest}"

if [ -z "$ACR_NAME" ]; then
    echo "❌ Error: ACR_NAME environment variable not set"
    echo "Usage: ACR_NAME=youracrname ./scripts/build-and-push.sh"
    exit 1
fi

echo "🏥 Building and pushing Docker image"
echo "======================================"
echo "ACR Name: $ACR_NAME"
echo "Image: $IMAGE_NAME:$IMAGE_TAG"
echo ""

# Login to Azure
echo "Logging in to Azure..."
az acr login --name "$ACR_NAME"
echo "✅ Logged in to ACR"

# Build image
echo ""
echo "Building Docker image..."
docker build -t "$ACR_NAME.azurecr.io/$IMAGE_NAME:$IMAGE_TAG" .
docker tag "$ACR_NAME.azurecr.io/$IMAGE_NAME:$IMAGE_TAG" "$ACR_NAME.azurecr.io/$IMAGE_NAME:latest"
echo "✅ Image built successfully"

# Push image
echo ""
echo "Pushing image to ACR..."
docker push "$ACR_NAME.azurecr.io/$IMAGE_NAME:$IMAGE_TAG"
docker push "$ACR_NAME.azurecr.io/$IMAGE_NAME:latest"
echo "✅ Image pushed successfully"

echo ""
echo "✅ Complete! Image available at: $ACR_NAME.azurecr.io/$IMAGE_NAME:$IMAGE_TAG"

