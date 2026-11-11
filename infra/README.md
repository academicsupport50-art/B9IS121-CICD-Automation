# Google Cloud setup

1. Create/select a Google Cloud project and enable billing.
2. Install Terraform >=1.6 and Google Cloud CLI.
3. Copy `terraform.tfvars.example` to `terraform.tfvars`; set project ID and exact GitHub OWNER/REPOSITORY.
4. Authenticate locally with `gcloud auth login`.
5. Run `terraform -chdir=infra init`, `plan -var-file=terraform.tfvars`, then review and `apply`.
6. Copy Terraform outputs into GitHub Actions repository variables:

- GCP_PROJECT_ID
- GCP_REGION
- GCP_AR_REPOSITORY
- GCP_WIF_PROVIDER
- GCP_DEPLOY_SA
- GCP_RUNTIME_SA

No service-account JSON key should be stored in GitHub. The pipeline uses GitHub OIDC and Google Workload Identity Federation.

The first Terraform apply creates a bootstrap Cloud Run service. The first successful workflow replaces it with the application image. The Cloud Run API is intentionally public for coursework testing and must contain no sensitive or privileged functionality.
