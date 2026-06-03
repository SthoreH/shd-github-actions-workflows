# ci-amplify-nodejs

Reusable CI workflow for Amplify Node.js repos.

Runs two parallel jobs:
- **Validate Application** — `npm ci`, `npm run lint`, `npx tsc --noEmit`
- **Validate Infrastructure** — `terraform fmt -check`, `init`, `validate`, `plan`

Both jobs read configuration from `.pipeline.yml` via `parse-config`. The `terraform-quality` job binds to the caller's GitHub Environment to access `secrets.AWS_ROLE_ARN` and `secrets.TF_STATE_BUCKET`.

## Inputs

| Name | Required | Description |
|------|----------|-------------|
| `environment` | yes | GitHub Environment name (`dev` or `prod`) |

## Secrets

| Name | Required | Description |
|------|----------|-------------|
| `github-token` | yes | GitHub PAT for Amplify repository access. Forwarded as `TF_VAR_github_token` for `terraform plan`. |

## `.pipeline.yml` keys consumed

| Key | Used by |
|-----|---------|
| `runtime.nodejs-version` | `actions/setup-node` |
| `app.working-path` | npm commands working directory |
| `infra.terraform-version` | `hashicorp/setup-terraform` |
| `infra.working-path` | `validate-terraform` working directory |

## Example caller

```yaml
jobs:
  pr-validate:
    runs-on: ubuntu-latest
    steps:
      - uses: SthoreH/shd-github-actions-workflows/actions/validate-pr@v1.7.0
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          validate-title: "false"
          validate-description: "false"

  ci:
    uses: SthoreH/shd-github-actions-workflows/.github/workflows/ci-amplify-nodejs.yml@v1.7.0
    with:
      environment: dev
    secrets:
      github-token: ${{ secrets.AMPLIFY_GITHUB_TOKEN }}
```
