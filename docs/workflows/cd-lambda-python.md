# cd-lambda-python.yml

Reusable workflow that packages a Python Lambda and applies its Terraform stack. Same flow used for first-class deploys (push to a branch) and rollbacks (re-deploy at a previous tag via the `ref` input).

Source: [.github/workflows/cd-lambda-python.yml](../../.github/workflows/cd-lambda-python.yml).

## Inputs

| Input | Required | Description |
|---|---|---|
| `environment` | yes | Target GitHub Environment. Binds the job to trigger environment protection rules (required reviewers, wait timers). |
| `ref` | no | Git ref (tag, branch, or SHA) to check out. Empty means the workflow's default ref. Used by rollback. |

## Job

Single job `deploy` (display name "Package & Deploy"):

1. Checkout (at `inputs.ref` if provided).
2. [parse-config](../actions/parse-config.md) — emit flattened config + files-to-replace.
3. Export config keys to env vars.
4. [replace-tokens](../actions/replace-tokens.md) — substitute env-specific values into source files.
5. [package-lambda-python](../actions/package-lambda-python.md) — build the `.zip`.
6. [deploy-terraform](../actions/deploy-terraform.md) — `terraform init` + `apply`, passing the zip as a tfvar.

## Required environment secrets

`secrets.AWS_ROLE_ARN`, `secrets.TF_STATE_BUCKET`. See [conventions](../conventions.md).

## Example callers

- Regular deploy: [app-aws-lbd-products-service/.github/workflows/deploy-dev.yml](../../../../app/app-aws-lbd-products-service/.github/workflows/deploy-dev.yml).
- Rollback (passes `ref`): [app-aws-lbd-products-service/.github/workflows/rollback.yml](../../../../app/app-aws-lbd-products-service/.github/workflows/rollback.yml).
