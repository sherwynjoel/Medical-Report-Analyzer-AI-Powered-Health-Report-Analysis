#!/bin/bash
# Deploy Medical Report Analyzer to Kubernetes

set -e

# Configuration
NAMESPACE="${NAMESPACE:-medical-analyzer}"
ACR_NAME="${ACR_NAME:-}"
RESOURCE_GROUP="${RESOURCE_GROUP:-medical-analyzer-rg}"
AKS_NAME="${AKS_NAME:-medical-analyzer-aks}"

if [ -z "$ACR_NAME" ]; then
    echo "❌ Error: ACR_NAME environment variable not set"
    exit 1
fi

echo "🏥 Deploying to Kubernetes"
echo "============================"
echo "Namespace: $NAMESPACE"
echo "ACR: $ACR_NAME"
echo "AKS: $AKS_NAME"
echo ""

# Get AKS credentials
echo "Getting AKS credentials..."
az aks get-credentials --resource-group "$RESOURCE_GROUP" --name "$AKS_NAME" --overwrite-existing
echo "✅ AKS credentials configured"

# Create namespace
echo ""
echo "Creating namespace..."
kubectl apply -f k8s/namespace.yaml
echo "✅ Namespace created"

# Create ACR secret
echo ""
echo "Creating ACR secret..."
ACR_PASSWORD=$(az acr credential show --name "$ACR_NAME" --query "passwords[0].value" -o tsv)

kubectl create secret docker-registry acr-secret \
  --docker-server="$ACR_NAME.azurecr.io" \
  --docker-username="$ACR_NAME" \
  --docker-password="$ACR_PASSWORD" \
  --namespace="$NAMESPACE" \
  --dry-run=client -o yaml | kubectl apply -f -
echo "✅ ACR secret created"

# Update deployment YAML
echo ""
echo "Updating deployment YAML..."
sed -i.bak "s|<ACR_LOGIN_SERVER>|$ACR_NAME.azurecr.io|g" k8s/deployment.yaml
rm -f k8s/deployment.yaml.bak
echo "✅ Deployment YAML updated"

# Deploy application
echo ""
echo "Deploying application..."
kubectl apply -f k8s/deployment.yaml
echo "✅ Application deployed"

# Wait for rollout
echo ""
echo "Waiting for deployment to be ready..."
kubectl rollout status deployment/medical-analyzer -n "$NAMESPACE" --timeout=5m
echo "✅ Deployment ready"

# Get service information
echo ""
echo "Service information:"
kubectl get service medical-analyzer-service -n "$NAMESPACE"

EXTERNAL_IP=$(kubectl get service medical-analyzer-service -n "$NAMESPACE" -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "")

if [ -n "$EXTERNAL_IP" ]; then
    echo ""
    echo "✅ Application is available at: http://$EXTERNAL_IP"
else
    echo ""
    echo "⚠️  External IP is being allocated. Check with:"
    echo "   kubectl get service medical-analyzer-service -n $NAMESPACE"
fi

