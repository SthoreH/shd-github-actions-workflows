# ci-infra-terraform.yml

Reusable workflow that validates a **pure infrastructure** repo (no application code) end-to-end: Terraform fmt + init + validate + plan against the target environment. Use it for repos that only provision AWS resources via Terraform — DynamoDB tables, ECS clusters, EventBridge buses, IAM roles, Cognito user pools, etc.

For repos with Lambda code, use [ci-lambda-python](ci-lambda-python.md) or [ci-lambda-nodejs](ci-lambda-nodejs.md) instead.

Source: [.github/workflows/ci-infra-terraform.yml](../../.github/workflows/ci-infra-terraform.yml).

## Inputs

| Input | Required | Description |
|---|---|---|
| `environment` | yes | Target GitHub Environment (e.g. `dev`, `prod`). Drives the parse-config selection and exposes `vars.*`. |

## Job

Single job `terraform-quality` (display name "Validate Infrastructure"):

1. Checkout
2. [parse-config](../actions/parse-config.md) — emit flattened config
3. Export config (`TF_VERSION`, `TF_PATH`)
4. [validate-terraform](../actions/validate-terraform.md) — fmt + init + validate + plan

## Required `.pipeline.yml` keys

| Flattened key | Source | Used for |
|---|---|---|
| `pipe_infra_terraform-version` | `infra.terraform-version` | setup-terraform |
| `pipe_infra_working-path` | `infra.working-path` | terraform working dir |

For pure infra, `runtime`, `deploy`, and `tests` sections are not required in `.pipeline.yml`.

## Required environment vars

`vars.AWS_ROLE_ARN`, `vars.TF_STATE_BUCKET`. See [conventions](../conventions.md).

## Example caller

```yaml
name: CI Dev
on:
  pull_request:
    branches: [dev]
permissions:
  contents: read
  id-token: write
jobs:
  pr-validate:
    name: Validate Pull Request
    runs-on: ubuntu-latest
    steps:
      - uses: SthoreH/shd-github-actions-workflows/actions/validate-pr@v1.6.0
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
  ci:
    name: Validate Infra
    uses: SthoreH/shd-github-actions-workflows/.github/workflows/ci-infra-terraform.yml@v1.6.0
    with:
      environment: dev
    secrets: inherit
```

A real example lives at [tpl-infra-aws-ddb/.github/workflows/ci-dev.yml](../../../../tpl/tpl-infra-aws-ddb/.github/workflows/ci-dev.yml).
