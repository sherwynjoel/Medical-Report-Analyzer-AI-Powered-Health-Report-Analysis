# Medical Report Analyzer - AI + DevOps Project

A comprehensive web application that uses AI to analyze medical reports, with full DevOps automation including CI/CD, containerization, infrastructure as code, and Kubernetes deployment on Azure AKS.

## 🎯 Project Overview

The Medical Report Analyzer is an AI-powered web application that:
- Accepts medical reports in PDF or text format
- Uses AI models (Hugging Face transformers) to analyze health indicators
- Provides a visual dashboard with risk assessment (low, moderate, high)
- Displays key findings and health metrics
- Automatically deploys to Azure Kubernetes Service (AKS) via CI/CD pipeline

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Repository                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │     Source Code (Frontend + Backend + AI/ML)         │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │ Push/PR
                     ▼
        ┌────────────────────────────┐
        │   GitHub Actions CI/CD     │
        │  ┌──────────────────────┐ │
        │  │ 1. Build Docker Image│ │
        │  │ 2. Push to ACR       │ │
        │  │ 3. Deploy to AKS     │ │
        │  └──────────────────────┘ │
        └────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌───────────────┐         ┌───────────────┐
│ Azure ACR     │         │  Azure AKS    │
│ (Container    │────────▶│  (Kubernetes) │
│  Registry)    │         │               │
└───────────────┘         └───────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  Load Balancer   │
                         │  (Public IP)     │
                         └──────────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  Web Application │
                         │  (Pods)          │
                         └──────────────────┘
```

## 🛠️ Technologies Stack

### Frontend
- HTML5, CSS3, JavaScript (Vanilla JS)
- Responsive design with modern UI/UX

### Backend
- Python 3.11
- Flask (REST API)
- Hugging Face Transformers (AI/ML)
- PyPDF2 (PDF text extraction)

### DevOps
- **Containerization**: Docker
- **Orchestration**: Kubernetes (AKS)
- **Infrastructure as Code**: Terraform
- **Configuration Management**: Ansible
- **CI/CD**: GitHub Actions
- **Cloud**: Microsoft Azure (AKS, ACR)

### AI/ML
- Hugging Face Transformers
- Text classification and summarization models

## 📁 Project Structure

```
Medical Report Analyzer/
│
├── backend/
│   ├── app.py              # Flask application
│   └── requirements.txt    # Python dependencies
│
├── frontend/
│   ├── index.html          # Main HTML page
│   ├── styles.css          # CSS styling
│   └── script.js           # Frontend JavaScript
│
├── terraform/
│   ├── main.tf             # Terraform main configuration
│   ├── variables.tf        # Terraform variables
│   ├── outputs.tf          # Terraform outputs
│   └── terraform.tfvars.example  # Example variables file
│
├── ansible/
│   ├── playbook.yml        # Ansible deployment playbook
│   └── requirements.yml    # Ansible collection requirements
│
├── k8s/
│   ├── deployment.yaml     # Kubernetes deployment manifest
│   ├── namespace.yaml      # Kubernetes namespace
│   └── acr-secret.yaml.example  # ACR secret example
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml       # GitHub Actions CI/CD pipeline
│
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose for local testing
├── .dockerignore          # Docker ignore file
│
├── README.md              # This file
├── SETUP.md               # Detailed setup instructions
└── DEPLOYMENT.md          # Deployment guide
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Azure CLI
- Terraform >= 1.0
- Ansible >= 2.9
- kubectl
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Medical-Report-Analyzer
   ```

2. **Set up Python environment**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Run locally**
   ```bash
   # From project root
   python backend/app.py
   ```
   Access at: http://localhost:5000

4. **Or use Docker Compose**
   ```bash
   docker-compose up --build
   ```

## 📦 Docker Usage

### Build Docker Image
```bash
docker build -t medical-analyzer:latest .
```

### Run Container
```bash
docker run -p 5000:5000 medical-analyzer:latest
```

## ☁️ Azure Deployment

### Step 1: Infrastructure Setup with Terraform

1. **Configure Terraform variables**
   ```bash
   cd terraform
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your values
   ```

2. **Initialize Terraform**
   ```bash
   terraform init
   ```

3. **Plan infrastructure**
   ```bash
   terraform plan
   ```

4. **Apply infrastructure**
   ```bash
   terraform apply
   ```

### Step 2: Build and Push Docker Image

1. **Login to Azure Container Registry**
   ```bash
   az acr login --name <your-acr-name>
   ```

2. **Build and push image**
   ```bash
   docker build -t <acr-name>.azurecr.io/medical-analyzer:latest .
   docker push <acr-name>.azurecr.io/medical-analyzer:latest
   ```

### Step 3: Deploy to AKS

#### Option A: Using kubectl

1. **Get AKS credentials**
   ```bash
   az aks get-credentials --resource-group <rg-name> --name <aks-name>
   ```

2. **Create namespace**
   ```bash
   kubectl apply -f k8s/namespace.yaml
   ```

3. **Create ACR secret**
   ```bash
   ACR_PASSWORD=$(az acr credential show --name <acr-name> --query "passwords[0].value" -o tsv)
   kubectl create secret docker-registry acr-secret \
     --docker-server=<acr-name>.azurecr.io \
     --docker-username=<acr-name> \
     --docker-password=$ACR_PASSWORD \
     --namespace=medical-analyzer
   ```

4. **Update deployment.yaml with your ACR name**
   ```bash
   # Edit k8s/deployment.yaml and replace <ACR_LOGIN_SERVER>
   ```

5. **Deploy application**
   ```bash
   kubectl apply -f k8s/deployment.yaml
   ```

6. **Check deployment status**
   ```bash
   kubectl get pods -n medical-analyzer
   kubectl get services -n medical-analyzer
   ```

#### Option B: Using Ansible

1. **Install Ansible collections**
   ```bash
   ansible-galaxy collection install -r ansible/requirements.yml
   ```

2. **Set environment variables**
   ```bash
   export ACR_LOGIN_SERVER="<your-acr>.azurecr.io"
   export IMAGE_TAG="latest"
   ```

3. **Run playbook**
   ```bash
   ansible-playbook ansible/playbook.yml \
     -e acr_login_server=$ACR_LOGIN_SERVER \
     -e image_tag=$IMAGE_TAG
   ```

### Step 4: Access Application

Get the external IP:
```bash
kubectl get service medical-analyzer-service -n medical-analyzer
```

Access the application at: `http://<EXTERNAL_IP>`

## 🔄 CI/CD Pipeline

The GitHub Actions workflow automatically:
1. Builds Docker image on push to main branch
2. Pushes to Azure Container Registry
3. Deploys to AKS cluster
4. Performs health checks

### Setup GitHub Secrets

Configure these secrets in your GitHub repository:
- `AZURE_CREDENTIALS`: Azure service principal credentials (JSON)
- `AZURE_SUBSCRIPTION_ID`: Azure subscription ID
- `ACR_NAME`: Azure Container Registry name
- `ACR_PASSWORD`: ACR admin password

See `DEPLOYMENT.md` for detailed setup instructions.

## 📊 Features

- **File Upload**: Support for PDF and TXT files
- **Text Analysis**: Direct text input analysis
- **AI-Powered Analysis**: 
  - Medical keyword extraction
  - Value range checking
  - Health risk assessment
  - Text summarization
- **Visual Dashboard**:
  - Risk level indicators (Low/Moderate/High)
  - Key findings cards
  - Analysis summary
- **Responsive Design**: Works on desktop and mobile

## 🔍 API Endpoints

- `GET /` - Serve frontend
- `GET /api/health` - Health check
- `POST /api/upload` - Upload and analyze file
- `POST /api/analyze` - Analyze text directly

## 🧪 Testing

### Local Testing
```bash
# Test API
curl http://localhost:5000/api/health

# Test file upload
curl -X POST -F "file=@sample-report.pdf" http://localhost:5000/api/upload
```

### Kubernetes Testing
```bash
# Port forward to test locally
kubectl port-forward service/medical-analyzer-service 8080:80 -n medical-analyzer
# Access at http://localhost:8080
```

## 📝 Configuration

### Environment Variables
- `PORT`: Server port (default: 5000)
- `FLASK_ENV`: Environment (development/production)
- `UPLOAD_FOLDER`: Upload directory path

### Azure Configuration
Edit `terraform/terraform.tfvars` to customize:
- Resource group name
- Location
- Node count
- VM size
- ACR name

## 🐛 Troubleshooting

### Common Issues

1. **AI models not loading**
   - Ensure sufficient disk space (models are ~500MB+)
   - Check internet connection for model download
   - First run downloads models automatically

2. **Docker build fails**
   - Check Docker daemon is running
   - Verify Dockerfile syntax
   - Check disk space

3. **AKS deployment fails**
   - Verify AKS credentials: `kubectl cluster-info`
   - Check ACR secret exists
   - Verify image name in deployment.yaml

4. **No external IP assigned**
   - Wait for LoadBalancer provisioning (can take 5-10 minutes)
   - Check AKS node resource limits

## 📚 Documentation

- [SETUP.md](SETUP.md) - Detailed setup instructions
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - Architecture documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is for educational purposes.

## 🙏 Acknowledgments

- Hugging Face for AI models
- Azure for cloud infrastructure
- Open source community




