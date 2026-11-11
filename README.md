# B9IS121 — CI/CD Automation and Cloud Deployment

**Module:** B9IS121 — Networks and Systems Administration  
**Programme:** MSc Cybersecurity  
**Repository:** https://github.com/academicsupport50-art/B9IS121-CICD-Automation

This repository implements a small CloudOps API and an automated pipeline that validates source changes, builds and scans a container image, publishes the verified image to Google Artifact Registry, and deploys it to Google Cloud Run.


## Architecture

GitHub commit or pull request → GitHub Actions → Ruff / Bandit / pip-audit / pytest → Docker build → Trivy image scan → Google Artifact Registry → Cloud Run → Postman HTTP verification.


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



pproval gates, automated rollback, SBOM generation, image signing, centralised monitoring, load testing and a documented disaster-recovery plan.
