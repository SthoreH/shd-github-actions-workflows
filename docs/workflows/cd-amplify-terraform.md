# cd-amplify-terraform

Reusable CD workflow for Amplify repos.

Runs a single deploy job: checkout (at optional `ref`) → `parse-config` → `replace-tokens` → `deploy-terraform` → `aws amplify start-job`.

Amplify's `enable_auto_build` must be set to `false` in Terraform so the Amplify build never races with `terraform apply`. This workflow triggers the build explicitly after the apply succeeds.

## Inputs

| Name | Required | Default | Description |
|------|----------|---------|-------------|
| `environment` | yes | — | GitHub Environment name (`dev` or `prod`) |
| `ref` | no | `''` | Git ref to deploy. Pass a tag for rollbacks. |

## Secrets

| Name | Required | Description |
|------|----------|-------------|
| `github-token` | yes | GitHub PAT for Amplify. Forwarded as `TF_VAR_github_token`. |
| `AWS_ROLE_ARN` | yes | AWS IAM role ARN to assume via OIDC. |
| `TF_STATE_BUCKET` | yes | S3 bucket for Terraform state backend. |

## `.pipeline.yml` keys consumed

| Key | Used by |
|-----|---------|
| `infra.terraform-version` | `deploy-terraform` action |
| `infra.working-path` | `deploy-terraform` working directory |
| `environments.<env>.files-to-replace` | `replace-tokens` action |

## Example caller (deploy)

```yaml
jobs:
  cd:
    uses: SthoreH/shd-github-actions-workflows/.github/workflows/cd-amplify-terraform.yml@v1.7.0
    with:
      environment: prod
    secrets:
      github-token: ${{ secrets.AMPLIFY_GITHUB_TOKEN }}
      AWS_ROLE_ARN: ${{ secrets.AWS_ROLE_ARN }}
      TF_STATE_BUCKET: ${{ secrets.TF_STATE_BUCKET }}
```

## Example caller (rollback)

```yaml
jobs:
  rollback:
    uses: SthoreH/shd-github-actions-workflows/.github/workflows/cd-amplify-terraform.yml@v1.7.0
    with:
      environment: ${{ needs.parse.outputs.environment }}
      ref: ${{ needs.parse.outputs.target_tag }}
    secrets:
      github-token: ${{ secrets.AMPLIFY_GITHUB_TOKEN }}
      AWS_ROLE_ARN: ${{ secrets.AWS_ROLE_ARN }}
      TF_STATE_BUCKET: ${{ secrets.TF_STATE_BUCKET }}
```
