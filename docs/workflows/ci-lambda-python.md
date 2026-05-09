# ci-lambda-python.yml

Reusable workflow that validates a Python Lambda repo: lint (non-blocking), tests (blocking), and Terraform fmt + init + validate + plan against the target environment. Called from a consumer's PR-triggered workflow with `environment` set to the target.

Source: [.github/workflows/ci-lambda-python.yml](../../.github/workflows/ci-lambda-python.yml).

## Inputs

| Input | Required | Description |
|---|---|---|
| `environment` | yes | Target GitHub Environment (e.g. `dev`, `prod`). Drives the parse-config selection and exposes `vars.*`. |

## Jobs

| Job ID | Display name | What it does |
|---|---|---|
| `python-quality` | Validate Application | Sets up Python (with pip cache), installs app + test requirements, runs `flake8` (non-blocking) and `pytest` (blocking). |
| `terraform-quality` | Validate Infrastructure | Calls [validate-terraform](../actions/validate-terraform.md) against the env's tfvars and state. |

## Required environment vars

For the `terraform-quality` job: `vars.AWS_ROLE_ARN`, `vars.TF_STATE_BUCKET`. See [conventions](../conventions.md).

## Example caller

[app-aws-lbd-products-service/.github/workflows/ci-dev.yml](../../../../app/app-aws-lbd-products-service/.github/workflows/ci-dev.yml).
