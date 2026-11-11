variable "project_id" {
  description = "Existing Google Cloud project ID with billing enabled."
  type        = string
}

variable "region" {
  description = "Cloud Run and Artifact Registry region."
  type        = string
  default     = "asia-south1"
}

variable "repository_id" {
  description = "Artifact Registry Docker repository name."
  type        = string
  default     = "b9is121-images"
}

variable "service_name" {
  description = "Cloud Run service name."
  type        = string
  default     = "b9is121-cloudops-api"
}

variable "github_repository" {
  description = "Exact GitHub repository in OWNER/REPOSITORY format."
  type        = string
  validation {
    condition     = can(regex("^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$", var.github_repository))
    error_message = "github_repository must use OWNER/REPOSITORY format."
  }
}

variable "wif_pool_id" {
  description = "Workload Identity Pool identifier."
  type        = string
  default     = "github-actions-pool"
}

variable "wif_provider_id" {
  description = "Workload Identity Provider identifier."
  type        = string
  default     = "github-oidc-provider"
}
