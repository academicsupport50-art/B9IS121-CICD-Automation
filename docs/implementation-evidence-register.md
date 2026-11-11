# Implementation evidence register

Status is deliberately conservative: only observed checks are marked as verified.

| Item | Status | Required proof |
|---|---|---|
| FastAPI application | Source committed; 9 local tests pass; 7 local HTTP smoke cases pass (200/404/422) | Repository source, pytest output and `docs/local-http-smoke-test-results.txt` |
| Automated tests | 9 tests passed in the preparation runtime | GitHub Actions test-step result is still required |
| Docker build | Not executed in the preparation runtime | Successful Docker build and local container response |
| Terraform | Configuration committed; not applied | Terraform fmt/validate/plan/apply output from the target project |
| GitHub Actions | Workflow committed; push runs have been created but are queued; first observed run's setup step reported failure | A completed successful validation job and accessible job logs |
| Artifact Registry | Not published | Image tag and digest from the actual registry |
| Cloud Run | Not deployed | Public HTTPS URL, active revision and service settings |
| Postman | Collection and example environment prepared; not run in Postman against a live endpoint | Actual request URLs, response bodies, status codes and assertion results |
| Commit-triggered update | Not demonstrated | Two source commits, two image tags, two Cloud Run revisions and matching build SHA values |
| Presentation | Slides and speaking script prepared; no recording | Unlisted YouTube or lecturer-accessible Google Drive video link |

The latest main-branch source commit is recorded in GitHub. At the last check, the newest Actions run was queued and the first run's only reported step was a failed job setup; no successful pipeline execution or cloud deployment is claimed. The job log retrieval did not complete, so the root cause of the runner setup issue is unknown.

Do not fabricate screenshots, logs, URLs, response results or a presentation recording. Update this register only when evidence is captured from the actual service or account.
