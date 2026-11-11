# B9IS121 — CI/CD Automation and Cloud Deployment

**Module:** B9IS121 — Networks and Systems Administration  
**Programme:** MSc Cybersecurity  
**Repository:** https://github.com/academicsupport50-art/B9IS121-CICD-Automation

This repository implements a small CloudOps API and an automated pipeline that validates source changes, builds and scans a container image, publishes the verified image to Google Artifact Registry, and deploys it to Google Cloud Run.

> **Evidence integrity:** The source and infrastructure configuration are committed. A successful remote pipeline, Artifact Registry publication, live Cloud Run URL, Postman run and commit-triggered revision update must be verified in the connected accounts before they are described as completed.

## Architecture

GitHub commit or pull request → GitHub Actions → Ruff / Bandit / pip-audit / pytest → Docker build → Trivy image scan → Google Artifact Registry → Cloud Run → Postman HTTP verification.

The pipeline transfers the exact image that passed the scan to the deployment job. It does not rebuild the image after scanning. GitHub OIDC and Google Workload Identity Federation provide short-lived cloud credentials; no service-account JSON key is required.

## Application

The FastAPI application is in `app/main.py`. It provides:

| Method | Endpoint | Purpose | Expected result |
|---|---|---|---|
| GET | `/` | API overview and endpoint links | 200 JSON |
| GET | `/healthz` | Health check | 200 JSON |
| GET | `/api/v1/info` | Version, environment and build SHA | 200 JSON |
| GET | `/api/v1/resources` | List five technology resources | 200 JSON |
| GET | `/api/v1/resources/{resource_id}` | Retrieve one resource | 200 or 404 |
| POST | `/api/v1/echo` | Validate and echo JSON | 200 or 422 |

FastAPI's generated API documentation is available at `/docs` when the service is running.

## Local checks

Use Python 3.12 or later:

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
ruff check app tests
bandit -q -r app -ll
pip-audit -r requirements.txt
pytest -q
```

Run locally with:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

Build and run the container:

```bash
docker build --pull -t b9is121-cloudops-api:local .
docker run --rm -p 8080:8080 b9is121-cloudops-api:local
```

Then open `http://localhost:8080/healthz`.

## Cloud infrastructure setup

Infrastructure is defined in Terraform under `infra/`. Review all files before applying; Terraform creates Google Cloud resources, service accounts, IAM bindings, a Workload Identity provider, Artifact Registry and a public Cloud Run service.

1. Create/select a dedicated Google Cloud project and enable billing. Review current Cloud Run and Artifact Registry prices and set a budget alert.
2. Install Terraform 1.6+ and Google Cloud CLI. Sign in with an account that has permission to create resources and modify IAM.
3. Copy `infra/terraform.tfvars.example` to `infra/terraform.tfvars`. Set the real project ID and the exact GitHub repository value `academicsupport50-art/B9IS121-CICD-Automation`. Keep `terraform.tfvars` private; it is ignored by Git.
4. Run:

```bash
terraform -chdir=infra init
terraform -chdir=infra validate
terraform -chdir=infra plan -var-file=terraform.tfvars
```

5. Review the plan carefully, then apply only after confirming the project, billing and IAM changes:

```bash
terraform -chdir=infra apply -var-file=terraform.tfvars
```

6. Copy the Terraform outputs into GitHub repository **Settings → Secrets and variables → Actions → Variables**:

| Variable | Terraform output / value |
|---|---|
| `GCP_PROJECT_ID` | Project ID used in `terraform.tfvars` |
| `GCP_REGION` | Selected region (default `asia-south1`) |
| `GCP_AR_REPOSITORY` | `b9is121-images` or `artifact_registry_repository` output suffix |
| `GCP_WIF_PROVIDER` | `workload_identity_provider` output |
| `GCP_DEPLOY_SA` | `deployer_service_account` output |
| `GCP_RUNTIME_SA` | `runtime_service_account` output |

7. Wait for IAM propagation and push a new commit to `main`. Open the repository's **Actions** tab and inspect both jobs. The deployment job must complete successfully before the Cloud Run URL is treated as live.
8. Copy the actual Cloud Run URL from the workflow summary and set the Postman collection's `baseUrl` variable to it (no trailing slash).

### Cost and security notes

The Terraform configuration creates a publicly invokable Cloud Run service because the assessment requires a public application. The sample API contains no authentication or private data. Keep it in a dedicated coursework project. Review the project-level IAM grants, restrict the WIF provider to the named repository and main branch, and do not reuse these identities in production. Cloud resources and stored images may incur charges; scale-to-zero does not guarantee zero cost.

## CI/CD pipeline

The workflow is `.github/workflows/ci-cd.yml` and runs for pull requests, pushes to `main`, and manual dispatch. It performs Ruff linting, Bandit static checks, pip-audit dependency auditing, pytest, Docker build and Trivy image scanning. On a successful main-branch push it transfers the exact scanned image to the deploy job, authenticates using OIDC federation, pushes the commit-SHA-tagged image to Artifact Registry, deploys to Cloud Run and verifies both `/healthz` and the deployed `build_sha`.

Third-party GitHub Actions used by the workflow are pinned to full 40-character commit SHAs. GitHub recommends full-length SHA pinning when workflow dependency lockfiles are not used, because it protects against mutable-tag changes. Terraform is installed before the workflow runs Terraform formatting and validation. The deploy job alone receives `id-token: write`. If the six Google Cloud repository variables are not yet configured, the workflow still runs validation, tests, Docker build and image scanning, then skips cloud deployment with an explanatory job summary.

## Postman

Import `postman/B9IS121_CloudOps_API.postman_collection.json`. Set the `baseUrl` collection variable to the actual Cloud Run URL, then run all requests. The collection tests health, service information, resource listing, resource lookup, missing-resource handling, valid echo and invalid echo. Expected negative responses are 404 and 422.

Capture actual request URLs, status codes, response bodies, response times and Postman test results. Expected outcomes are not evidence of a successful remote test.

## Submission evidence checklist

- [ ] GitHub Actions validation job: lint, Bandit, dependency audit and tests.
- [ ] Trivy scan output and commit-SHA image in Artifact Registry.
- [ ] Cloud Run deployment success and public service URL.
- [ ] Browser access to the live API and `/docs`.
- [ ] Postman request/response screenshots and assertion results.
- [ ] A second source commit producing a new Cloud Run revision; record both commit SHAs/revisions.
- [ ] 7–10 minute presentation video, uploaded as an unlisted YouTube video or accessible Google Drive video.
- [ ] Final PDF report with architecture, rationale, real screenshots, repository URL, video link and critical evaluation.

Use `docs/implementation-evidence-register.md` to track what has actually been verified. Do not fabricate logs, screenshots, URLs or results.

## Limitations and improvements

This is a focused coursework API, not a production service. It has no persistent database, user authentication, custom domain, multi-region failover, formal penetration-test evidence or load-test evidence. Improvements could include staging/production promotion, approval gates, automated rollback, SBOM generation, image signing, centralised monitoring, load testing and a documented disaster-recovery plan.
