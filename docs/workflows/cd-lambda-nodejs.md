# cd-lambda-nodejs.yml

Reusable workflow that packages a Node.js Lambda (TypeScript or JavaScript) and applies its Terraform stack. Same flow used for first-class deploys (push to a branch) and rollbacks (re-deploy at a previous tag via the `ref` input).

Source: [.github/workflows/cd-lambda-nodejs.yml](../../.github/workflows/cd-lambda-nodejs.yml).

## Inputs

| Input | Required | Description |
|---|---|---|
| `environment` | yes | Target GitHub Environment. Binds the job to expose `vars.*` and trigger any environment protection rules. |
| `ref` | no | Git ref (tag, branch, or SHA) to check out. Empty means the workflow's default ref. Used by rollback. |

## Job

Single job `deploy` (display name "Package & Deploy"):

1. Checkout (at `inputs.ref` if provided).
2. [parse-config](../actions/parse-config.md) — emit flattened config + files-to-replace.
3. Export config keys to env vars.
4. [replace-tokens](../actions/replace-tokens.md) — substitute env-specific values into source files.
5. [package-lambda-nodejs](../actions/package-lambda-nodejs.md) — esbuild bundle + zip.
6. [deploy-terraform](../actions/deploy-terraform.md) — `terraform init` + `apply`.

## Required `.pipeline.yml` keys

Same as [ci-lambda-nodejs.yml](ci-lambda-nodejs.md): `pipe_runtime_nodejs-version`, `pipe_deploy_working-path`, `pipe_deploy_entry`, `pipe_infra_terraform-version`, `pipe_infra_working-path`.

## Required environment vars

`vars.AWS_ROLE_ARN`, `vars.TF_STATE_BUCKET`. See [conventions](../conventions.md).

## Example callers

Pattern identical to the Python equivalent — regular deploy and rollback (passes `ref`). See [cd-lambda-python.md](cd-lambda-python.md).
