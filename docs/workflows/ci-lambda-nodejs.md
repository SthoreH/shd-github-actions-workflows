# ci-lambda-nodejs.yml

Reusable workflow that validates a Node.js Lambda repo: lint (non-blocking), tests (blocking), and Terraform fmt + init + validate + plan against the target environment. Called from a consumer's PR-triggered workflow with `environment` set to the target.

Source: [.github/workflows/ci-lambda-nodejs.yml](../../.github/workflows/ci-lambda-nodejs.yml).

## Inputs

| Input | Required | Description |
|---|---|---|
| `environment` | yes | Target GitHub Environment (e.g. `dev`, `prod`). Drives the parse-config selection and triggers environment protection rules. |

## Jobs

| Job ID | Display name | What it does |
|---|---|---|
| `nodejs-quality` | Validate Application | Sets up pnpm + Node (with pnpm cache), installs deps with `pnpm install --frozen-lockfile`, runs `pnpm run lint` (non-blocking) and `pnpm test` (blocking). |
| `terraform-quality` | Validate Infrastructure | Calls [package-lambda-nodejs](../actions/package-lambda-nodejs.md) so the artifact exists for `filebase64sha256`, then [validate-terraform](../actions/validate-terraform.md) against the env's tfvars and state. |

## Required `.pipeline.yml` keys

The workflow reads these flattened keys from [parse-config](../actions/parse-config.md):

| Flattened key | Source | Used for |
|---|---|---|
| `pipe_runtime_nodejs-version` | `runtime.nodejs-version` | setup-node + esbuild target |
| `pipe_deploy_working-path` | `deploy.working-path` | where `package.json` lives |
| `pipe_deploy_entry` | `deploy.entry` | esbuild entry file |
| `pipe_infra_terraform-version` | `infra.terraform-version` | setup-terraform |
| `pipe_infra_working-path` | `infra.working-path` | terraform working dir |

## Required environment secrets

For the `terraform-quality` job: `secrets.AWS_ROLE_ARN`, `secrets.TF_STATE_BUCKET`. See [conventions](../conventions.md).

## Example caller

A consumer wrapper (PR validation) — pattern identical to the Python equivalent, see [ci-lambda-python.md](ci-lambda-python.md).
