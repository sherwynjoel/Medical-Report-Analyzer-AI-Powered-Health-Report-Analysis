# CI/CD Pipeline Integration - Medical Report Analyzer

## 📍 Location of CI/CD Pipeline

**File Path**: `.github/workflows/ci-cd.yml`

This file is automatically detected by GitHub Actions when you push code to GitHub.

---

## 🔄 How It's Integrated

### 1. **Automatic Detection**
- GitHub Actions automatically finds workflows in `.github/workflows/` directory
- File name can be anything, but `.yml` or `.yaml` extension is required
- Multiple workflow files can exist

### 2. **Triggered Automatically**
The pipeline triggers on:
- ✅ **Push to main/master branch** - Full build and deployment
- ✅ **Pull Requests** - Build and test only (no deployment)
- ✅ **Manual trigger** - Via GitHub Actions UI (`workflow_dispatch`)

### 3. **Integration Points**

```
┌─────────────────────────────────────────────────────────────┐
│                    GITHUB REPOSITORY                        │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  .github/workflows/ci-cd.yml  ← Pipeline Definition │ │
│  └──────────────────────────────────────────────────────┘ │
│                           │                                │
│                           ▼                                │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  Code Push / PR → Triggers Workflow                  │ │
│  └──────────────────────────────────────────────────────┘ │
└─────────────────────────────┬─────────────────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   GITHUB ACTIONS     │
                    │   (CI/CD Runner)     │
                    └──────────────────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
         ┌──────────────────┐  ┌──────────────────┐
         │  Build Job       │  │  Deploy Job      │
         │  (Always runs)   │  │  (On main only)  │
         └──────────────────┘  └──────────────────┘
                    │                     │
                    ▼                     ▼
         ┌──────────────────┐  ┌──────────────────┐
         │  Build Docker    │  │  Deploy to AKS   │
         │  Push to ACR     │  │  Kubernetes      │
         │  Security Scan   │  │  Health Check    │
         └──────────────────┘  └──────────────────┘
```

---

## 📋 Pipeline Workflow Steps

### Job 1: Build and Push (Always Runs)
1. ✅ **Checkout code** - Gets latest code from repository
2. ✅ **Setup Docker Buildx** - Prepares Docker builder
3. ✅ **Login to Azure** - Authenticates with Azure
4. ✅ **Login to ACR** - Authenticates with Azure Container Registry
5. ✅ **Build Docker Image** - Creates container image
6. ✅ **Push to ACR** - Uploads image to Azure Container Registry
7. ✅ **Security Scan** - Runs Trivy vulnerability scanner
8. ✅ **Upload Results** - Reports security findings

### Job 2: Deploy to AKS (Only on Push to Main)
1. ✅ **Checkout code** - Gets latest code
2. ✅ **Login to Azure** - Authenticates with Azure
3. ✅ **Setup kubectl** - Installs Kubernetes CLI
4. ✅ **Get AKS Credentials** - Connects to Kubernetes cluster
5. ✅ **Create Namespace** - Sets up Kubernetes namespace
6. ✅ **Create ACR Secret** - Configures image pull authentication
7. ✅ **Deploy to Kubernetes** - Applies deployment manifests
8. ✅ **Wait for Rollout** - Ensures deployment completes
9. ✅ **Get Service Endpoint** - Retrieves public IP address
10. ✅ **Health Check** - Verifies application is running

---

## 🔍 How to View CI/CD Pipeline

### 1. **On GitHub Website**
1. Go to: https://github.com/sherwynjoel/Medical-Report-Analyzer-AI-Powered-Health-Report-Analysis
2. Click **"Actions"** tab (top navigation)
3. See all workflow runs
4. Click any run to see detailed logs

### 2. **Pipeline Status Badge** (Optional)
Add this to your README.md:
```markdown
![CI/CD Pipeline](https://github.com/sherwynjoel/Medical-Report-Analyzer-AI-Powered-Health-Report-Analysis/workflows/CI/CD%20Pipeline/badge.svg)
```

---

## ⚙️ Configuration Required

### GitHub Secrets (Required for Pipeline to Work)

Go to: `Repository → Settings → Secrets and variables → Actions`

Add these secrets:

1. **AZURE_CREDENTIALS** 
   ```json
   {
     "clientId": "...",
     "clientSecret": "...",
     "subscriptionId": "...",
     "tenantId": "..."
   }
   ```

2. **AZURE_SUBSCRIPTION_ID**
   - Your Azure subscription ID

3. **ACR_NAME**
   - Your Azure Container Registry name

4. **ACR_PASSWORD**
   - ACR admin password

---

## 🚀 How Pipeline Works

### Scenario 1: Push to Main Branch
```
Developer pushes code
        ↓
GitHub Actions triggers
        ↓
Build Docker image
        ↓
Push to Azure Container Registry
        ↓
Deploy to Azure Kubernetes Service (AKS)
        ↓
Application is live!
```

### Scenario 2: Pull Request
```
Developer creates PR
        ↓
GitHub Actions triggers
        ↓
Build Docker image (test build)
        ↓
Security scan
        ↓
Results shown in PR
        ↓
No deployment (waits for merge)
```

---

## 📁 Files Used by Pipeline

The CI/CD pipeline uses these project files:

```
.github/workflows/ci-cd.yml    ← Pipeline definition
├── Dockerfile                  ← Used for building image
├── k8s/deployment.yaml         ← Used for Kubernetes deployment
├── k8s/namespace.yaml          ← Used for namespace creation
└── backend/                    ← Application code to package
```

---

## ✅ Verification

### Check if Pipeline is Active:
1. Go to GitHub repository
2. Click "Actions" tab
3. You should see workflow runs (or "Set up workflow" if not configured)

### Test the Pipeline:
1. Make any change to code
2. Commit and push:
   ```bash
   git add .
   git commit -m "Test CI/CD"
   git push origin main
   ```
3. Go to Actions tab
4. Watch the pipeline run!

---

## 📊 Pipeline Status

- ✅ **Pipeline File**: Created and in correct location
- ✅ **Triggers**: Configured (push, PR, manual)
- ✅ **Jobs**: Build and Deploy jobs defined
- ⚠️ **Secrets**: Need to be configured in GitHub
- ⚠️ **Azure Resources**: Need to be created first (via Terraform)

---

## 🔗 Integration Summary

**The CI/CD pipeline is fully integrated in the project:**

1. **Location**: `.github/workflows/ci-cd.yml`
2. **Type**: GitHub Actions (native GitHub CI/CD)
3. **Auto-detection**: Yes, GitHub finds it automatically
4. **Status**: Ready to use (needs GitHub secrets configured)
5. **Integration**: Tightly integrated with Azure and Kubernetes

**Once you configure GitHub secrets and Azure resources, every push to main will automatically build and deploy your application!**

