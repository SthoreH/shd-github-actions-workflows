# cd-infra-terraform.yml

Reusable workflow that applies a Terraform stack for a **pure infrastructure** repo. Same flow used for first-class deploys (push to a branch) and rollbacks (re-deploy at a previous tag via the `ref` input). No application packaging step.

For repos with Lambda code, use [cd-lambda-python](cd-lambda-python.md) or [cd-lambda-nodejs](cd-lambda-nodejs.md) instead.

Source: [.github/workflows/cd-infra-terraform.yml](../../.github/workflows/cd-infra-terraform.yml).

## Inputs

| Input | Required | Description |
|---|---|---|
| `environment` | yes | Target GitHub Environment. Binds the job to trigger environment protection rules (required reviewers, wait timers). |
| `ref` | no | Git ref (tag, branch, or SHA) to check out. Empty means the workflow's default ref. Used by rollback. |

## Job

Single job `deploy` (display name "Deploy Infrastructure"):

1. Checkout (at `inputs.ref` if provided)
2. [parse-config](../actions/parse-config.md) — emit flattened config + files-to-replace
3. Export config keys to env vars
4. [replace-tokens](../actions/replace-tokens.md) — substitute env-specific values into source files (no-op when `files-to-replace` is empty)
5. [deploy-terraform](../actions/deploy-terraform.md) — `terraform init` + `apply`

## Required `.pipeline.yml` keys

Same as [ci-infra-terraform.yml](ci-infra-terraform.md): `pipe_infra_terraform-version`, `pipe_infra_working-path`.

## Required environment secrets

`secrets.AWS_ROLE_ARN`, `secrets.TF_STATE_BUCKET`. See [conventions](../conventions.md).

## Example callers

```yaml
# Regular deploy
name: Deploy Dev
on:
  push:
    branches: [dev]
    paths:
      - "terraform-aws/**"
      - ".github/**"
permissions:
  contents: read
  id-token: write
jobs:
  cd:
    name: Deploy Infra
    uses: SthoreH/shd-github-actions-workflows/.github/workflows/cd-infra-terraform.yml@v1.6.0
    with:
      environment: dev
    secrets: inherit
```

For rollback (passing `ref`), see the pattern in [tpl-infra-aws-ddb/.github/workflows/rollback.yml](../../../../tpl/tpl-infra-aws-ddb/.github/workflows/rollback.yml).
