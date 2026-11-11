# Implementation evidence register

This register distinguishes repository artefacts from execution evidence. A committed configuration file proves that the configuration exists; it does not prove that a remote build or deployment succeeded.

| Assessment item | Current status | Evidence required before claiming completion |
|---|---|---|
| FastAPI application | Source committed | Repository source and local/CI test result |
| Automated tests | Nine tests are included; latest remote run has not yet been verified | Successful pytest job log and JUnit artifact |
| Python static security | Bandit and pip-audit configured | Successful job output and audit report |
| Docker build | Configured in GitHub Actions; remote execution pending | Successful Docker build step |
| Terraform configuration | Committed; CI formatting and validation configured | Successful Terraform fmt and validate steps |
| GitHub Actions | Workflow committed; latest observed run is queued | Completed successful workflow run and job logs |
| Trivy image scan | Configured to fail on HIGH/CRITICAL findings | Scan report for the exact image later deployed |
| Artifact Registry image | Not published / not verified | Commit-SHA image tag and digest in registry |
| Google Cloud infrastructure | Terraform prepared; not applied | Successful Terraform apply and outputs |
| Cloud Run | Not deployed / not verified | Public HTTPS URL and active revision |
| Postman | Collection committed; no live run verified | Actual endpoint URL, HTTP status, response body, response time and passing assertions |
| Commit-triggered update | Not demonstrated | Two distinct source commits linked to two Cloud Run revisions |
| Presentation video | Slides and script prepared | 7–10 minute unlisted YouTube or accessible Drive URL |

## Evidence integrity rule

Never invent screenshots, test logs, cloud URLs, image digests, HTTP responses or deployment outcomes. Update this register only after the relevant step has been executed and independently checked.
