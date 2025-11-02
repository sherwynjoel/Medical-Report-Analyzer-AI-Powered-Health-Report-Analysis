variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "medical-analyzer"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "eastus"
}

variable "node_count" {
  description = "Number of AKS nodes"
  type        = number
  default     = 2
}

variable "vm_size" {
  description = "VM size for AKS nodes"
  type        = string
  default     = "Standard_D2s_v3"
}

variable "acr_name" {
  description = "Azure Container Registry name (must be globally unique, lowercase alphanumeric)"
  type        = string
}

