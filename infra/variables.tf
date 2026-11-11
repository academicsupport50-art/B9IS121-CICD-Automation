variable "project_id" {
  description = "Google Cloud project ID with billing enabled."
  type = string
}
variable "region" {
  description = "Cloud Run and Artifact Registry region."
  type = string
  default = "asia-south1"
}
variable "repository_id" {
  type = string
  default = "b9is121-images"
}
variable "service_name" {
  type = string
  default = "b9is121-cloudops-api"
}
variable "github_repository" {
  description = "Exact GitHub OWNER/REPOSITORY."
  type = string
  validation {
    condition = can(regex("^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$", var.github_repository))
    error_message = "Use OWNER/REPOSITORY format."
  }
}
