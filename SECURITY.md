# Security notes

- The deployment job requests `id-token: write` only when deploying and authenticates through Workload Identity Federation.
- The WIF provider condition restricts trust to the configured repository and `refs/heads/main`.
- The runtime service account is separate from the deployer identity and receives no additional project roles.
- The deployer receives Artifact Registry Writer on the single image repository, Cloud Run Developer on the single service, Service Usage Consumer on the project, and Service Account User on the runtime identity.
- The container runs as UID/GID 10001, uses a multi-stage build, excludes development files and secrets from the image context, and does not embed credentials.
- Trivy scans the built image for HIGH and CRITICAL vulnerabilities. The configured pipeline fails on findings at those levels when reported by the scanner.
- `pip-audit` checks pinned Python dependencies; Bandit performs a static source scan.
- The Cloud Run API is intentionally public for assessment validation. It exposes only non-sensitive metadata, static demonstration data and a validated echo endpoint.
- The public service IAM binding is managed by Terraform. The deployment workflow does not receive permission to change IAM policy.
- Cloud Run revisions support traffic rollback. Confirm the selected previous revision is healthy before routing all traffic to it.
- GitHub Actions currently use version tags for readability. A production implementation should pin third-party actions to reviewed full commit SHAs.
