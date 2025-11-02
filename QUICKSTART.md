# Quick Start Guide - Medical Report Analyzer

Get started in 5 minutes!

## 🚀 Quick Local Test

### Option 1: Python (Recommended for Development)

```bash
# 1. Install dependencies
pip install -r backend/requirements.txt

# 2. Run application
python backend/app.py

# 3. Open browser
# http://localhost:5000
```

### Option 2: Docker

```bash
# Build and run
docker-compose up --build

# Access at http://localhost:5000
```

## ☁️ Quick Azure Deployment

### 1. Infrastructure (5-10 minutes)

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your ACR name (must be unique)

terraform init
terraform apply  # Type 'yes' when prompted
```

### 2. Build and Push Image (5 minutes)

```bash
# Login to ACR
az acr login --name <your-acr-name>

# Build and push
docker build -t <acr-name>.azurecr.io/medical-analyzer:latest .
docker push <acr-name>.azurecr.io/medical-analyzer:latest
```

### 3. Deploy to AKS (5 minutes)

```bash
# Get credentials
az aks get-credentials --resource-group medical-analyzer-rg --name medical-analyzer-aks

# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create ACR secret
ACR_NAME="<your-acr-name>"
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)
kubectl create secret docker-registry acr-secret \
  --docker-server=${ACR_NAME}.azurecr.io \
  --docker-username=$ACR_NAME \
  --docker-password=$ACR_PASSWORD \
  --namespace=medical-analyzer

# Update and deploy
sed -i "s|<ACR_LOGIN_SERVER>|${ACR_NAME}.azurecr.io|g" k8s/deployment.yaml
kubectl apply -f k8s/deployment.yaml

# Get IP
kubectl get service medical-analyzer-service -n medical-analyzer
```

## 🔄 Quick CI/CD Setup

1. Push to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

2. Configure GitHub Secrets:
   - Go to: Settings > Secrets > Actions
   - Add: `AZURE_CREDENTIALS`, `AZURE_SUBSCRIPTION_ID`, `ACR_NAME`, `ACR_PASSWORD`

3. Update `.github/workflows/ci-cd.yml` with your values

4. Push again - pipeline auto-runs!

## 📋 Common Commands

```bash
# Health check
curl http://localhost:5000/api/health

# Kubernetes logs
kubectl logs -f deployment/medical-analyzer -n medical-analyzer

# Scale deployment
kubectl scale deployment medical-analyzer --replicas=3 -n medical-analyzer

# Port forward (local testing)
kubectl port-forward service/medical-analyzer-service 8080:80 -n medical-analyzer

# Delete deployment
kubectl delete -f k8s/deployment.yaml
```

## 🐛 Quick Troubleshooting

**Application not starting?**
```bash
kubectl logs deployment/medical-analyzer -n medical-analyzer
```

**Image pull errors?**
```bash
kubectl get secret acr-secret -n medical-analyzer
```

**No external IP?**
```bash
kubectl describe service medical-analyzer-service -n medical-analyzer
```

**Terraform errors?**
```bash
az login
az account set --subscription "<subscription-id>"
```

## 📚 Full Documentation

- [README.md](README.md) - Overview
- [SETUP.md](SETUP.md) - Detailed setup
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- [CHECKLIST.md](CHECKLIST.md) - Deployment checklist

---

**Need help?** Check the troubleshooting sections in the detailed guides!

