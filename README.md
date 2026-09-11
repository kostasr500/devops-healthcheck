# DevOps URL - Health Check

A simple health-check tool for websites: a Python CLI script, containerized with Docker, tested and built through GitHub Actions on every push, and deployed to Azure through Terraform, with the image automatically pushed to a container registry when changes land on `main`.

## What it does

`src/health_check.py` sends a request to a URL and reports back whether it's healthy, using the standard library's `argparse` for the CLI options:

```bash
python src/health_check.py --url https://httpbin.org/status/200 --timeout 5
```

It also supports `--json` if you want machine-readable output instead of plain text, and it measures round-trip latency so you can see how fast the endpoint responded.

It exits with different codes depending on the result, which matters if you're chaining it into scripts or monitoring:

- `0` — endpoint responded with a 2xx status (healthy)
- `1` — endpoint responded but with a 4xx/5xx status (unhealthy)
- `2` — request failed outright (timeout, DNS failure, connection error)

## Running it with Docker

```bash
docker build -t devops-healthcheck:local .
docker run --rm devops-healthcheck:local --url https://httpbin.org/status/200 --timeout 5
```

A couple of things I paid attention to in the Dockerfile: it's built on `python:3.12-slim` to keep the image small, it copies `requirements.txt` and installs dependencies before copying the rest of the code so Docker can cache that layer between builds, and it runs as a non-root user (`appuser`) instead of root.

## CI/CD pipeline

There are two GitHub Actions workflows:

- **`ci.yml`** runs on pull requests to `main` and on pushes to `feat/**` branches. It first runs the Python checks (installs dependencies, runs the CLI against a test endpoint, checks the exit codes behave correctly), then builds the Docker image and runs a smoke test with it.
- **`cd.yml`** only runs on merges to `main` (or manually via `workflow_dispatch`). It logs into Azure Container Registry using secrets stored in GitHub (`ACR_USERNAME`, `ACR_PASSWORD`), then builds and pushes the image tagged both with the commit SHA and `latest`.

The idea was to keep testing and deployment separate, nothing gets pushed to the registry unless it's actually merged.

## Infrastructure with Terraform

The `terraform/` folder provisions everything needed to run this in Azure:

- A resource group (`rg-devops-healthcheck-dev`)
- A Container Registry (`acrhealthcheckkostas`, Basic SKU)
- A Container Instance (`aci-devops-healthcheck-dev`) that runs the image once and stops (`restart_policy = "Never"`), since this is a one-shot check rather than a long-running service

```bash
cd terraform
terraform init
terraform plan
terraform apply
terraform destroy   # to tear it down and stop paying for it
```

You'll need the Azure CLI logged in (`az login`) and Terraform installed. Check `variables.tf` for what you can configure, like the target URL or environment name.

## Project structure

```
.
├── .github/workflows/
│   ├── ci.yml            # tests + docker build on PRs
│   └── cd.yml            # builds and pushes image to ACR on merge to main
├── src/
│   └── health_check.py   # the actual health check CLI
├── terraform/
│   ├── main.tf            # resource group, ACR, container instance
│   ├── outputs.tf
│   ├── providers.tf
│   └── variables.tf
├── .dockerignore
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```
