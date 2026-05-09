# destroy-terraform

Runs `terraform init` (with backend config) and `destroy -auto-approve` against a target environment. Generic — not tied to Lambda. Use for any IaC stack that needs a tear-down path.

Source: [actions/destroy-terraform/action.yml](../../actions/destroy-terraform/action.yml).

## Inputs

| Input | Required | Default | Description |
|---|---|---|---|
| `environment` | yes | — | Drives `environments/<env>.tfvars`. |
| `working-directory` | no | `terraform-aws` | Terraform root module. |
| `terraform-version` | no | `1.14.8` | Terraform CLI version. |
| `tf-backend-bucket` | yes | — | S3 bucket for state. |
| `tf-backend-key` | yes | — | State object key. Convention: `{repo-name}/terraform.tfstate`. |
| `aws-role-arn` | yes | — | IAM role assumed via OIDC. |
| `aws-region` | no | `sa-east-1` | AWS region. |

## Outputs

None.

## Caller requirements

Job must declare `permissions: id-token: write`. If the stack declares required variables (e.g. `lambda_zip_path` for a Lambda), give them safe defaults so `destroy` doesn't need build-time inputs.

## Example usage

[app-aws-lbd-products-service/.github/workflows/destroy.yml](../../../../app/app-aws-lbd-products-service/.github/workflows/destroy.yml).
