# Conventions

Shared rules every reusable workflow and composite action in this repo relies on. Consumer repos must follow these for the pipeline to function.

## `.pipeline.yml` schema

Lives at the consumer repo root. Parsed by [parse-config](actions/parse-config.md), which merges the global blocks with the selected environment and flattens everything into `pipe_<section>_<key>` JSON keys.

| Section | Purpose | Flattened keys |
|---|---|---|
| `runtime` | Lambda runtime version. Set the key matching your stack: `python-version` or `nodejs-version`. | `pipe_runtime_python-version` **or** `pipe_runtime_nodejs-version` |
| `infra` | IaC tool version and root module path. | `pipe_infra_terraform-version`, `pipe_infra_working-path` |
| `deploy` | Source code root and per-runtime build inputs. | Python: `pipe_deploy_working-path`, `pipe_deploy_requirements`. Node.js: `pipe_deploy_working-path`, `pipe_deploy_entry`. |
| `tests` | Test root (and test requirements for Python). | Python: `pipe_tests_working-path`, `pipe_tests_requirements`. Node.js: `pipe_tests_working-path`. |
| `environments.<env>` | Per-environment values (only the selected env is merged). | `pipe_environment_<key>` |
| `environments.files-to-replace` | List of files for token substitution at CD time. | Exposed separately as the `files_to_replace` output. |

Real examples:
- Python — [app-aws-lbd-products-service/.pipeline.yml](../../../app/app-aws-lbd-products-service/.pipeline.yml).
- Node.js — [tpl-app-aws-lbd-nodejs/.pipeline.yml](../../../tpl/tpl-app-aws-lbd-nodejs/.pipeline.yml).

## GitHub Environment vars (per env)

Set these on each GitHub Environment (`Settings → Environments`). They are read at workflow run time when the job declares `environment: <name>`:

- `AWS_ROLE_ARN` — IAM role assumed via OIDC.
- `TF_STATE_BUCKET` — S3 bucket holding the Terraform state for that environment. Buckets are typically per-account.

Both are non-secret variables (`vars.*`), not secrets.

## OIDC trust

Each role configured in `vars.AWS_ROLE_ARN` must trust the GitHub Actions OIDC provider, scoped to the consumer repo (and ideally to specific environments / branches via the `sub` claim). Without this, [validate-terraform](actions/validate-terraform.md), [deploy-terraform](actions/deploy-terraform.md), and [destroy-terraform](actions/destroy-terraform.md) fail at the credentials step.

The caller job must declare `permissions: id-token: write` so GitHub mints the OIDC token.

## Terraform backend

Partial backend config injected at `terraform init -backend-config=...`. Consumers set `terraform { backend "s3" {} }` in `provider.tf` (no bucket / key inline).

- **Bucket** — `vars.TF_STATE_BUCKET` (per environment).
- **Key** — `{repo-name}/terraform.tfstate` (one state per repo per env, since buckets are segregated by account).
- **Region** — `sa-east-1` by default; overridable per action call.

## Workflow permissions baseline

Caller workflows should set `permissions: contents: read` at the workflow level. Jobs that need OIDC additionally declare `id-token: write` at the job level. Avoid blanket `write-all`.

## Tagging

This repo uses semantic-release. Consumers pin reusable workflows and actions to a tagged release (`@v1.4.0`, etc.). `@main` is acceptable while developing this repo locally but should never land in a consumer's production pipeline.

## Token replacement

`environments.files-to-replace` in `.pipeline.yml` lists files (relative to repo root) that [replace-tokens](actions/replace-tokens.md) processes during CD. Tokens have the form `${pipe_environment_role-arn}` etc. — keys come from the flattened JSON described above. Only files in this list are touched.
