# Setup Guide - Medical Report Analyzer

This guide provides step-by-step instructions to set up and deploy the Medical Report Analyzer project.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Setup](#docker-setup)
4. [Azure Setup](#azure-setup)
5. [Terraform Infrastructure](#terraform-infrastructure)
6. [Ansible Configuration](#ansible-configuration)
7. [GitHub Actions CI/CD](#github-actions-cicd)
8. [Verification](#verification)

## Prerequisites

### Required Tools

1. **Python 3.11+**
   ```bash
   python --version
   # Should be 3.11 or higher
   ```

2. **Docker & Docker Compose**
   ```bash
   docker --version
   docker-compose --version
   ```

3. **Azure CLI**
   ```bash
   az --version
   # Install: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
   ```

4. **Terraform >= 1.0**
   ```bash
   terraform --version
   # Install: https://www.terraform.io/downloads
   ```

5. **Ansible >= 2.9**
   ```bash
   ansible --version
   # Install: pip install ansible
   ```

6. **kubectl**
   ```bash
   kubectl version --client
   # Install: https://kubernetes.io/docs/tasks/tools/
   ```

7. **Git**
   ```bash
   git --version
   ```

### Azure Account Setup

1. Create an Azure account at https://azure.microsoft.com/
2. Create a subscription (or use existing)
3. Install Azure CLI and login:
   ```bash
   az login
   az account set --subscription "<subscription-id>"
   ```

## Local Development Setup

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd Medical-Report-Analyzer
```

### 2. Create Python Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Note**: First installation will download AI models (~500MB+). This may take several minutes.

### 4. Create Upload Directory

```bash
mkdir -p uploads
```

### 5. Run Application

```bash
# From project root
python backend/app.py
```

Access at: http://localhost:5000

## Docker Setup

### 1. Build Docker Image

```bash
docker build -t medical-analyzer:latest .
```

### 2. Run with Docker

```bash
docker run -p 5000:5000 medical-analyzer:latest
```

### 3. Run with Docker Compose

```bash
docker-compose up --build
```

Access at: http://localhost:5000

## Azure Setup

### 1. Login to Azure

```bash
az login
az account list
az account set --subscription "<your-subscription-id>"
```

### 2. Create Service Principal for GitHub Actions

```bash
az ad sp create-for-rbac --name "medical-analyzer-sp" \
  --role contributor \
  --scopes /subscriptions/<subscription-id> \
  --sdk-auth
```

Save the JSON output as `AZURE_CREDENTIALS` GitHub secret.

### 3. Get ACR Admin Password

After creating ACR (via Terraform):
```bash
az acr credential show --name <acr-name>
```

Save the password as `ACR_PASSWORD` GitHub secret.

## Terraform Infrastructure

### 1. Navigate to Terraform Directory

```bash
cd terraform
```

### 2. Configure Variables

```bash
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars`:
```hcl
project_name = "medical-analyzer"
location     = "eastus"  # or your preferred region
node_count   = 2
vm_size      = "Standard_D2s_v3"
acr_name     = "youruniqueacrname"  # Must be globally unique, lowercase, alphanumeric only
```

**Important**: ACR name must be globally unique and lowercase alphanumeric (no hyphens).

### 3. Initialize Terraform

```bash
terraform init
```

### 4. Review Plan

```bash
terraform plan
```

### 5. Apply Infrastructure

```bash
terraform apply
```

Type `yes` when prompted. This will create:
- Resource Group
- Azure Container Registry (ACR)
- Virtual Network
- Subnet
- AKS Cluster
- Role assignments

**Note**: AKS cluster creation takes 10-15 minutes.

### 6. Get Outputs

```bash
terraform output
```

Save these values:
- `acr_login_server`
- `aks_cluster_name`
- `resource_group_name`

### 7. Configure kubectl

```bash
az aks get-credentials \
  --resource-group <resource-group-name> \
  --name <aks-cluster-name> \
  --overwrite-existing
```

Verify connection:
```bash
kubectl cluster-info
kubectl get nodes
```

## Build and Push Docker Image

### 1. Login to ACR

```bash
az acr login --name <acr-name>
```

### 2. Tag Image

```bash
docker tag medical-analyzer:latest <acr-name>.azurecr.io/medical-analyzer:latest
```

### 3. Push Image

```bash
docker push <acr-name>.azurecr.io/medical-analyzer:latest
```

## Ansible Configuration

### 1. Install Ansible Collections

```bash
ansible-galaxy collection install -r ansible/requirements.yml
```

### 2. Update Playbook Variables

Edit `ansible/playbook.yml` if needed, or pass as extra vars.

### 3. Run Playbook

```bash
ansible-playbook ansible/playbook.yml \
  -e acr_login_server="<acr-name>.azurecr.io" \
  -e image_tag="latest" \
  -e replicas=2 \
  -e namespace="medical-analyzer"
```

## Manual Kubernetes Deployment

### 1. Create Namespace

```bash
kubectl apply -f k8s/namespace.yaml
```

### 2. Create ACR Secret

```bash
ACR_PASSWORD=$(az acr credential show --name <acr-name> --query "passwords[0].value" -o tsv)

kubectl create secret docker-registry acr-secret \
  --docker-server=<acr-name>.azurecr.io \
  --docker-username=<acr-name> \
  --docker-password=$ACR_PASSWORD \
  --namespace=medical-analyzer
```

### 3. Update Deployment YAML

Edit `k8s/deployment.yaml` and replace `<ACR_LOGIN_SERVER>` with your ACR login server:
```yaml
image: <acr-name>.azurecr.io/medical-analyzer:latest
```

### 4. Deploy Application

```bash
kubectl apply -f k8s/deployment.yaml
```

### 5. Check Status

```bash
kubectl get pods -n medical-analyzer
kubectl get services -n medical-analyzer
```

### 6. Get External IP

```bash
kubectl get service medical-analyzer-service -n medical-analyzer
```

Wait for `EXTERNAL-IP` to be assigned (may take 5-10 minutes).

## GitHub Actions CI/CD

### 1. Create GitHub Repository

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2. Configure GitHub Secrets

Go to: `Settings > Secrets and variables > Actions`

Add these secrets:

- **AZURE_CREDENTIALS**: Service principal JSON (from Azure setup)
  ```json
  {
    "clientId": "...",
    "clientSecret": "...",
    "subscriptionId": "...",
    "tenantId": "..."
  }
  ```

- **AZURE_SUBSCRIPTION_ID**: Your Azure subscription ID

- **ACR_NAME**: Your ACR name (without .azurecr.io)

- **ACR_PASSWORD**: ACR admin password

### 3. Update Workflow File

Edit `.github/workflows/ci-cd.yml` and update:
- `AZURE_RESOURCE_GROUP`: Your resource group name
- `AKS_CLUSTER_NAME`: Your AKS cluster name

### 4. Test Pipeline

Push to main branch:
```bash
git add .
git commit -m "Setup CI/CD"
git push origin main
```

Check Actions tab in GitHub to see pipeline execution.

## Verification

### 1. Check Application Health

```bash
# Local
curl http://localhost:5000/api/health

# Kubernetes
EXTERNAL_IP=$(kubectl get service medical-analyzer-service -n medical-analyzer -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
curl http://$EXTERNAL_IP/api/health
```

### 2. Test File Upload

Open browser and navigate to application URL.

### 3. Check Logs

```bash
# Local Docker
docker logs <container-id>

# Kubernetes
kubectl logs -f deployment/medical-analyzer -n medical-analyzer
```

### 4. Scale Deployment (Optional)

```bash
kubectl scale deployment medical-analyzer --replicas=3 -n medical-analyzer
```

## Troubleshooting

### Issue: Terraform authentication fails
```bash
az login
az account set --subscription "<subscription-id>"
```

### Issue: kubectl connection fails
```bash
az aks get-credentials --resource-group <rg-name> --name <aks-name> --overwrite-existing
```

### Issue: Docker push fails
```bash
az acr login --name <acr-name>
az acr credential show --name <acr-name>
```

### Issue: Pods in CrashLoopBackOff
```bash
kubectl describe pod <pod-name> -n medical-analyzer
kubectl logs <pod-name> -n medical-analyzer
```

### Issue: No external IP assigned
```bash
# Check LoadBalancer service
kubectl describe service medical-analyzer-service -n medical-analyzer

# Check node resources
kubectl top nodes
```

## Next Steps

1. Set up monitoring and logging
2. Configure custom domain
3. Set up SSL/TLS certificates
4. Implement database for report history
5. Add authentication

## Additional Resources

- [Azure AKS Documentation](https://docs.microsoft.com/azure/aks/)
- [Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)

