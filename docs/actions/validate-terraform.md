# validate-terraform

Runs `terraform fmt -check`, `init` (with backend config), `validate`, and `plan` against a target environment. Used by CI to confirm the Terraform stack is sound before merge.

Source: [actions/validate-terraform/action.yml](../../actions/validate-terraform/action.yml).

## Inputs

| Input | Required | Default | Description |
|---|---|---|---|
| `environment` | yes | — | Drives the per-env tfvars file: `environments/<env>.tfvars`. |
| `working-directory` | no | `terraform-aws` | Path to the Terraform root module. |
| `terraform-version` | no | `1.14.8` | Terraform CLI version. |
| `tf-backend-bucket` | yes | — | S3 bucket for state. Typically `vars.TF_STATE_BUCKET`. |
| `tf-backend-key` | yes | — | State object key. Org convention: `{repo-name}/terraform.tfstate`. |
| `aws-role-arn` | yes | — | IAM role assumed via OIDC. |
| `aws-region` | no | `sa-east-1` | AWS region. |

## Outputs

None.

## Caller requirements

The job must declare `permissions: id-token: write` for OIDC. See [conventions](../conventions.md).

## Example usage

[ci-lambda-python.yml](../../.github/workflows/ci-lambda-python.yml).
