# Cloud deployment setup and verification

## Before applying Terraform

- Use a dedicated Google Cloud coursework project.
- Confirm billing and create a budget alert.
- Review `infra/main.tf`, especially the service accounts, IAM roles, Workload Identity Federation condition and public Cloud Run invoker binding.
- Set `project_id`, region and exact GitHub repository in a local `infra/terraform.tfvars` file. Do not commit this file.

## Apply

```bash
terraform -chdir=infra init
terraform -chdir=infra validate
terraform -chdir=infra plan -var-file=terraform.tfvars
terraform -chdir=infra apply -var-file=terraform.tfvars
```

The first apply creates the registry, identities, OIDC trust configuration and a temporary Cloud Run service using Google's sample hello image. The first successful CI/CD deployment replaces that image with the application container.

## GitHub Actions variables

Add these six variables under **Settings → Secrets and variables → Actions → Variables**:

- `GCP_PROJECT_ID`
- `GCP_REGION`
- `GCP_AR_REPOSITORY`
- `GCP_WIF_PROVIDER`
- `GCP_DEPLOY_SA`
- `GCP_RUNTIME_SA`

Use the exact values from Terraform outputs. The WIF provider is restricted to the repository configured in `github_repository` and the `main` branch. No service-account key is needed.

## Verify

If the six GitHub repository variables are not yet present, the workflow deliberately completes CI validation and skips the cloud deployment job. Configure all six variables before expecting Artifact Registry publication and Cloud Run deployment.


After IAM propagation, push a new commit to `main`. Confirm that the GitHub Actions validation job passes all lint, security, dependency, test, build and scan steps. Then confirm that the deploy job publishes the same scanned image and completes Cloud Run deployment.

Use the URL in the Actions job summary to check `/healthz`, `/api/v1/info` and `/docs`. The information endpoint must report the same commit SHA as the workflow run. Import the Postman collection and record actual HTTP statuses, response bodies, response times and assertion results.

## Cost and cleanup

Cloud Run and Artifact Registry can incur charges. Review current pricing, create a budget alert and remove unused resources after the assessment if they are no longer needed. Terraform destroy removes resources managed by this state; inspect the destroy plan carefully before approving it.
