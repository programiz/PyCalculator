variable "subscription_id" {
  description = "The Subscription ID where the AKS cluster will be created"
  type        = string
}

variable "client_id" {
  description = "The Client ID for the Service Principal"
  type        = string
}

variable "client_secret" {
  description = "The Client Secret for the Service Principal"
  type        = string
}

variable "tenant_id" {
  description = "The Tenant ID associated with the Service Principal"
  type        = string
}

variable "resource_group_name" {
  description = "The name of the Resource Group"
  type        = string
  default     = "aks-acr-rg"
}

variable "location" {
  description = "The location/region where the resources will be created"
  type        = string
  default     = "East US"
}

variable "aks_cluster_name" {
  description = "The name of the AKS Cluster"
  type        = string
  default     = "myAKSCluster"
}

variable "acr_name" {
  description = "The name of the Azure Container Registry"
  type        = string
  default     = "myContainerRegistry"
}

variable "node_count" {
  description = "The initial number of nodes in the AKS Cluster"
  type        = number
  default     = 3
}

variable "vm_size" {
  description = "The size of the VM instances"
  type        = string
  default     = "Standard_DS2_v2"
}
