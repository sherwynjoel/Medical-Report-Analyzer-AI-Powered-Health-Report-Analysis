# Deployment Checklist - Medical Report Analyzer

Use this checklist to ensure all steps are completed for successful deployment.

## Prerequisites ✅

- [ ] Azure account created and active
- [ ] Azure subscription active
- [ ] Azure CLI installed (`az --version`)
- [ ] Azure CLI logged in (`az login`)
- [ ] Terraform >= 1.0 installed (`terraform --version`)
- [ ] Ansible >= 2.9 installed (`ansible --version`)
- [ ] kubectl installed (`kubectl version --client`)
- [ ] Docker installed (`docker --version`)
- [ ] Git installed (`git --version`)
- [ ] Python 3.11+ installed (`python --version`)

## Local Development Setup ✅

- [ ] Repository cloned
- [ ] Python virtual environment created
- [ ] Dependencies installed (`pip install -r backend/requirements.txt`)
- [ ] Application runs locally (`python backend/app.py`)
- [ ] Application accessible at http://localhost:5000
- [ ] File upload functionality tested
- [ ] Text analysis functionality tested

## Docker Setup ✅

- [ ] Docker image builds successfully (`docker build -t medical-analyzer .`)
- [ ] Docker container runs locally (`docker run -p 5000:5000 medical-analyzer`)
- [ ] Docker Compose works (`docker-compose up`)

## Azure Infrastructure (Terraform) ✅

- [ ] Terraform initialized (`terraform init`)
- [ ] `terraform.tfvars` configured with your values
- [ ] Terraform plan reviewed (`terraform plan`)
- [ ] Terraform apply successful (`terraform apply`)
- [ ] Resource group created
- [ ] Azure Container Registry (ACR) created
- [ ] AKS cluster created and running
- [ ] Virtual network and subnet created
- [ ] Terraform outputs saved

## Azure Container Registry ✅

- [ ] ACR name configured (globally unique)
- [ ] ACR admin enabled
- [ ] Docker login to ACR successful (`az acr login`)
- [ ] Docker image tagged correctly
- [ ] Docker image pushed to ACR (`docker push`)
- [ ] Image visible in ACR portal

## Kubernetes Configuration ✅

- [ ] kubectl configured for AKS (`az aks get-credentials`)
- [ ] Kubernetes cluster connection verified (`kubectl cluster-info`)
- [ ] Nodes visible and ready (`kubectl get nodes`)
- [ ] Namespace created (`kubectl apply -f k8s/namespace.yaml`)
- [ ] ACR secret created in Kubernetes
- [ ] Deployment YAML updated with ACR name
- [ ] Deployment applied (`kubectl apply -f k8s/deployment.yaml`)
- [ ] Pods running (`kubectl get pods`)
- [ ] Service created and LoadBalancer IP assigned
- [ ] Application accessible via external IP

## Ansible Deployment (Optional) ✅

- [ ] Ansible collections installed (`ansible-galaxy collection install -r ansible/requirements.yml`)
- [ ] Playbook variables configured
- [ ] Playbook execution successful (`ansible-playbook ansible/playbook.yml`)
- [ ] Deployment verified in Kubernetes

## GitHub Actions CI/CD ✅

- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] GitHub Actions enabled
- [ ] Service principal created for Azure
- [ ] GitHub secrets configured:
  - [ ] `AZURE_CREDENTIALS`
  - [ ] `AZURE_SUBSCRIPTION_ID`
  - [ ] `ACR_NAME`
  - [ ] `ACR_PASSWORD`
- [ ] GitHub Actions workflow file updated with correct values
- [ ] Pipeline triggered on push
- [ ] Build job successful
- [ ] Deploy job successful
- [ ] Application automatically deployed after push

## Verification ✅

- [ ] Health endpoint responds (`curl http://<EXTERNAL_IP>/api/health`)
- [ ] Frontend loads correctly in browser
- [ ] File upload works
- [ ] Text analysis works
- [ ] Results display correctly
- [ ] Dashboard shows risk levels
- [ ] Findings are displayed

## Testing ✅

- [ ] Test with PDF file
- [ ] Test with TXT file
- [ ] Test with direct text input
- [ ] Test error handling (invalid files, large files)
- [ ] Test health check endpoint
- [ ] Test with multiple concurrent requests

## Monitoring & Logging ✅

- [ ] Application logs accessible (`kubectl logs`)
- [ ] Pod status checked (`kubectl get pods`)
- [ ] Resource usage monitored (`kubectl top pods`)
- [ ] Service endpoints verified
- [ ] Error logs reviewed

## Documentation ✅

- [ ] README.md reviewed
- [ ] SETUP.md reviewed
- [ ] DEPLOYMENT.md reviewed
- [ ] Architecture documented
- [ ] Screenshots captured (for project report)
- [ ] Commands documented
- [ ] Troubleshooting notes added

## Project Report ✅

- [ ] Project overview written
- [ ] Architecture diagram created
- [ ] Step-by-step deployment documented
- [ ] Screenshots included:
  - [ ] Local application running
  - [ ] Terraform infrastructure
  - [ ] AKS cluster
  - [ ] Kubernetes deployment
  - [ ] Application on Azure
  - [ ] CI/CD pipeline execution
- [ ] Commands documented with outputs
- [ ] Challenges and solutions documented

## Demo Video ✅

- [ ] Video script prepared
- [ ] Demo flow: Code push → Pipeline → Deployment → Web access
- [ ] All components shown:
  - [ ] GitHub repository
  - [ ] CI/CD pipeline execution
  - [ ] Docker build
  - [ ] ACR push
  - [ ] Kubernetes deployment
  - [ ] Application access
  - [ ] File upload and analysis
  - [ ] Results display
- [ ] Video recorded and edited
- [ ] Video uploaded (YouTube/Vimeo/Drive)

## Cleanup (Optional) ✅

- [ ] Test resources deleted
- [ ] Development resources cleaned up
- [ ] Production resources retained
- [ ] Cost monitoring enabled

## Final Checklist ✅

- [ ] All components working
- [ ] Documentation complete
- [ ] Project report ready
- [ ] Demo video ready
- [ ] Code pushed to GitHub
- [ ] Repository public/shared with instructor
- [ ] Ready for submission

---

## Quick Command Reference

```bash
# Local Development
python backend/app.py

# Docker
docker build -t medical-analyzer .
docker run -p 5000:5000 medical-analyzer

# Terraform
cd terraform
terraform init
terraform plan
terraform apply

# ACR
az acr login --name <acr-name>
docker push <acr-name>.azurecr.io/medical-analyzer:latest

# Kubernetes
az aks get-credentials --resource-group <rg> --name <aks-name>
kubectl apply -f k8s/deployment.yaml
kubectl get pods -n medical-analyzer
kubectl get services -n medical-analyzer

# CI/CD
git push origin main  # Triggers pipeline
```

---

**Last Updated**: See commit history for latest updates

