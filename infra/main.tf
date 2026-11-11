provider "google" {
  project = var.project_id
  region  = var.region
}

locals {
  apis = toset([
    "artifactregistry.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "iam.googleapis.com",
    "iamcredentials.googleapis.com",
    "run.googleapis.com",
    "serviceusage.googleapis.com",
    "sts.googleapis.com"
  ])
}

resource "google_project_service" "apis" {
  for_each = local.apis
  project = var.project_id
  service = each.value
  disable_on_destroy = false
}

resource "google_artifact_registry_repository" "images" {
  project = var.project_id
  location = var.region
  repository_id = var.repository_id
  description = "B9IS121 application container images"
  format = "DOCKER"
  depends_on = [google_project_service.apis]
}

resource "google_service_account" "runtime" {
  project = var.project_id
  account_id = "b9is121-runtime"
  display_name = "B9IS121 Cloud Run runtime identity"
}

resource "google_service_account" "deployer" {
  project = var.project_id
  account_id = "b9is121-deployer"
  display_name = "B9IS121 GitHub Actions deployer"
}

resource "google_iam_workload_identity_pool" "github" {
  project = var.project_id
  workload_identity_pool_id = "github-actions-pool"
  display_name = "GitHub Actions pool"
  depends_on = [google_project_service.apis]
}

resource "google_iam_workload_identity_pool_provider" "github" {
  project = var.project_id
  workload_identity_pool_id = google_iam_workload_identity_pool.github.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-oidc-provider"
  display_name = "GitHub OIDC provider"
  attribute_mapping = {
    "google.subject" = "assertion.sub"
    "attribute.repository" = "assertion.repository"
    "attribute.ref" = "assertion.ref"
  }
  attribute_condition = "assertion.repository == '${var.github_repository}' && assertion.ref == 'refs/heads/main'"
  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

resource "google_service_account_iam_member" "wif_user" {
  service_account_id = google_service_account.deployer.name
  role = "roles/iam.workloadIdentityUser"
  member = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github.name}/attribute.repository/${var.github_repository}"
}

resource "google_artifact_registry_repository_iam_member" "writer" {
  project = var.project_id
  location = google_artifact_registry_repository.images.location
  repository = google_artifact_registry_repository.images.name
  role = "roles/artifactregistry.writer"
  member = "serviceAccount:${google_service_account.deployer.email}"
}

resource "google_service_account_iam_member" "act_as_runtime" {
  service_account_id = google_service_account.runtime.name
  role = "roles/iam.serviceAccountUser"
  member = "serviceAccount:${google_service_account.deployer.email}"
}

resource "google_project_iam_member" "service_usage" {
  project = var.project_id
  role = "roles/serviceusage.serviceUsageConsumer"
  member = "serviceAccount:${google_service_account.deployer.email}"
}

resource "google_cloud_run_v2_service" "api" {
  project = var.project_id
  name = var.service_name
  location = var.region
  ingress = "INGRESS_TRAFFIC_ALL"
  template {
    service_account = google_service_account.runtime.email
    max_instance_request_concurrency = 80
    scaling {
      min_instance_count = 0
      max_instance_count = 3
    }
    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello"
      ports { container_port = 8080 }
      resources {
        limits = {
          cpu = "1"
          memory = "512Mi"
        }
      }
      env { name = "APP_ENV", value = "production" }
      env { name = "BUILD_SHA", value = "terraform-bootstrap" }
    }
  }
  depends_on = [google_project_service.apis, google_artifact_registry_repository.images]
}

resource "google_cloud_run_v2_service_iam_member" "public" {
  project = var.project_id
  location = google_cloud_run_v2_service.api.location
  name = google_cloud_run_v2_service.api.name
  role = "roles/run.invoker"
  member = "allUsers"
}

resource "google_cloud_run_v2_service_iam_member" "deployer" {
  project = var.project_id
  location = google_cloud_run_v2_service.api.location
  name = google_cloud_run_v2_service.api.name
  role = "roles/run.developer"
  member = "serviceAccount:${google_service_account.deployer.email}"
}
