# Deployment Guide - Medical Report Analyzer

Complete guide for deploying the Medical Report Analyzer to Azure Kubernetes Service (AKS).

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Deployment Flow                         │
└─────────────────────────────────────────────────────────────┘

1. Code Push to GitHub
        ↓
2. GitHub Actions Triggered
        ↓
3. Build Docker Image
        ↓
4. Push to Azure Container Registry (ACR)
        ↓
5. Deploy to Azure Kubernetes Service (AKS)
        ↓
6. Application Available via LoadBalancer IP
```

## Prerequisites Checklist

- [ ] Azure subscription active
- [ ] Azure CLI installed and logged in
- [ ] Terraform >= 1.0 installed
- [ ] kubectl installed
- [ ] Docker installed
- [ ] GitHub repository created
- [ ] GitHub Actions enabled

## Step-by-Step Deployment

### Phase 1: Infrastructure Provisioning

#### 1.1 Terraform Initialization

```bash
cd terraform
terraform init
```

#### 1.2 Configure Variables

```bash
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars`:
```hcl
project_name = "medical-analyzer"
location     = "eastus"
node_count   = 2
vm_size      = "Standard_D2s_v3"
acr_name     = "youruniqueacr123"  # Must be unique globally
```

#### 1.3 Validate Configuration

```bash
terraform validate
terraform plan
```

#### 1.4 Apply Infrastructure

```bash
terraform apply
```

**Expected Output:**
- Resource Group: `medical-analyzer-rg`
- ACR: `<acr-name>.azurecr.io`
- AKS Cluster: `medical-analyzer-aks`
- Virtual Network and Subnet

**Duration**: 10-15 minutes

#### 1.5 Save Outputs

```bash
terraform output > terraform-outputs.txt
```

### Phase 2: Container Image Preparation

#### 2.1 Configure kubectl

```bash
az aks get-credentials \
  --resource-group medical-analyzer-rg \
  --name medical-analyzer-aks \
  --overwrite-existing
```

#### 2.2 Login to ACR

```bash
az acr login --name <acr-name>
```

#### 2.3 Build and Push Image

```bash
# Build
docker build -t <acr-name>.azurecr.io/medical-analyzer:latest .

# Tag
docker tag medical-analyzer:latest <acr-name>.azurecr.io/medical-analyzer:latest

# Push
docker push <acr-name>.azurecr.io/medical-analyzer:latest
```

**Note**: First push may take 5-10 minutes (large image with AI models).

### Phase 3: Kubernetes Deployment

#### 3.1 Create Namespace

```bash
kubectl apply -f k8s/namespace.yaml
```

#### 3.2 Create ACR Secret

```bash
ACR_NAME="<your-acr-name>"
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)

kubectl create secret docker-registry acr-secret \
  --docker-server=${ACR_NAME}.azurecr.io \
  --docker-username=$ACR_NAME \
  --docker-password=$ACR_PASSWORD \
  --namespace=medical-analyzer
```

#### 3.3 Update Deployment YAML

Edit `k8s/deployment.yaml`:
```yaml
image: <acr-name>.azurecr.io/medical-analyzer:latest
```

Or use sed:
```bash
sed -i "s|<ACR_LOGIN_SERVER>|${ACR_NAME}.azurecr.io|g" k8s/deployment.yaml
```

#### 3.4 Deploy Application

```bash
kubectl apply -f k8s/deployment.yaml
```

#### 3.5 Verify Deployment

```bash
# Check pods
kubectl get pods -n medical-analyzer

# Check services
kubectl get services -n medical-analyzer

# Check deployment status
kubectl rollout status deployment/medical-analyzer -n medical-analyzer
```

#### 3.6 Get External IP

```bash
kubectl get service medical-analyzer-service -n medical-analyzer
```

Wait for `EXTERNAL-IP` assignment (5-10 minutes).

### Phase 4: CI/CD Setup

#### 4.1 Create Service Principal

```bash
SUBSCRIPTION_ID=$(az account show --query id -o tsv)

az ad sp create-for-rbac \
  --name "medical-analyzer-sp" \
  --role contributor \
  --scopes /subscriptions/$SUBSCRIPTION_ID \
  --sdk-auth
```

Save the JSON output.

#### 4.2 Configure GitHub Secrets

Go to: `Repository > Settings > Secrets and variables > Actions`

Add secrets:

1. **AZURE_CREDENTIALS**
   - Value: JSON output from service principal creation

2. **AZURE_SUBSCRIPTION_ID**
   - Value: Your Azure subscription ID
   ```bash
   az account show --query id -o tsv
   ```

3. **ACR_NAME**
   - Value: Your ACR name (without .azurecr.io)

4. **ACR_PASSWORD**
   - Value: ACR admin password
   ```bash
   az acr credential show --name <acr-name> --query "passwords[0].value" -o tsv
   ```

#### 4.3 Update GitHub Actions Workflow

Edit `.github/workflows/ci-cd.yml`:

Update these variables in the `env` section:
```yaml
env:
  AZURE_RESOURCE_GROUP: medical-analyzer-rg
  ACR_NAME: ${{ secrets.ACR_NAME }}
  AKS_CLUSTER_NAME: medical-analyzer-aks
```

#### 4.4 Test CI/CD Pipeline

```bash
git add .
git commit -m "Setup CI/CD pipeline"
git push origin main
```

Monitor in: `Repository > Actions`

### Phase 5: Verification

#### 5.1 Health Check

```bash
EXTERNAL_IP=$(kubectl get service medical-analyzer-service -n medical-analyzer -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

curl http://$EXTERNAL_IP/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "medical-report-analyzer",
  "models_loaded": true
}
```

#### 5.2 Test Application

1. Open browser: `http://<EXTERNAL_IP>`
2. Upload a test PDF or text file
3. Verify analysis results appear

#### 5.3 Check Logs

```bash
# Application logs
kubectl logs -f deployment/medical-analyzer -n medical-analyzer

# All pods logs
kubectl logs -f -l app=medical-analyzer -n medical-analyzer
```

## Deployment Methods Comparison

### Method 1: Manual Deployment (kubectl)
- ✅ Full control
- ✅ Good for learning
- ❌ Manual steps
- ❌ No automation

### Method 2: Ansible Playbook
- ✅ Infrastructure as Code
- ✅ Repeatable
- ❌ Requires Ansible knowledge

### Method 3: GitHub Actions CI/CD
- ✅ Fully automated
- ✅ Triggered on git push
- ✅ Best for production
- ✅ Integrated with GitHub

**Recommended**: Use GitHub Actions CI/CD for production.

## Scaling

### Scale Up Deployment

```bash
kubectl scale deployment medical-analyzer --replicas=4 -n medical-analyzer
```

### Horizontal Pod Autoscaler

Create `k8s/hpa.yaml`:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: medical-analyzer-hpa
  namespace: medical-analyzer
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: medical-analyzer
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

Apply:
```bash
kubectl apply -f k8s/hpa.yaml
```

## Rollback

### Rollback Deployment

```bash
# View deployment history
kubectl rollout history deployment/medical-analyzer -n medical-analyzer

# Rollback to previous version
kubectl rollout undo deployment/medical-analyzer -n medical-analyzer

# Rollback to specific revision
kubectl rollout undo deployment/medical-analyzer --to-revision=2 -n medical-analyzer
```

## Monitoring

### View Pod Status

```bash
kubectl get pods -n medical-analyzer -w
```

### Resource Usage

```bash
kubectl top pods -n medical-analyzer
kubectl top nodes
```

### Describe Resources

```bash
kubectl describe deployment medical-analyzer -n medical-analyzer
kubectl describe service medical-analyzer-service -n medical-analyzer
```

## Troubleshooting Deployment

### Pods Not Starting

```bash
# Check pod events
kubectl describe pod <pod-name> -n medical-analyzer

# Check logs
kubectl logs <pod-name> -n medical-analyzer

# Common issues:
# - Image pull errors: Check ACR secret
# - Resource limits: Check node capacity
# - Startup errors: Check application logs
```

### Image Pull Errors

```bash
# Verify ACR secret
kubectl get secret acr-secret -n medical-analyzer

# Recreate secret if needed
ACR_PASSWORD=$(az acr credential show --name <acr-name> --query "passwords[0].value" -o tsv)
kubectl create secret docker-registry acr-secret \
  --docker-server=<acr-name>.azurecr.io \
  --docker-username=<acr-name> \
  --docker-password=$ACR_PASSWORD \
  --namespace=medical-analyzer \
  --dry-run=client -o yaml | kubectl apply -f -
```

### Service Not Getting External IP

```bash
# Check service events
kubectl describe service medical-analyzer-service -n medical-analyzer

# Check if LoadBalancer is supported in your region
# Some regions may require additional configuration
```

### Application Not Responding

```bash
# Check pod health
kubectl get pods -n medical-analyzer

# Check application logs
kubectl logs -f deployment/medical-analyzer -n medical-analyzer

# Port forward for testing
kubectl port-forward service/medical-analyzer-service 8080:80 -n medical-analyzer
# Test: http://localhost:8080
```

## Cleanup

### Delete Deployment

```bash
kubectl delete -f k8s/deployment.yaml
kubectl delete -f k8s/namespace.yaml
```

### Destroy Infrastructure

```bash
cd terraform
terraform destroy
```

**Warning**: This will delete all resources!

## Production Considerations

1. **SSL/TLS**: Configure HTTPS with Azure Application Gateway or cert-manager
2. **Monitoring**: Set up Azure Monitor or Prometheus
3. **Logging**: Configure Azure Log Analytics
4. **Backup**: Regular ACR image backups
5. **Security**: Enable Azure Policy, RBAC, network policies
6. **Database**: Add persistent storage for report history
7. **CDN**: Use Azure CDN for static assets
8. **Cost Optimization**: Use Spot instances for non-critical workloads

## Next Steps

1. Set up monitoring and alerting
2. Configure custom domain
3. Implement authentication
4. Add database for report storage
5. Set up backup and disaster recovery

---

For setup instructions, see [SETUP.md](SETUP.md)

