# deploy-terraform

Runs `terraform init` (with backend config) and `apply -auto-approve` against a target environment. Receives the Lambda artifact path as a tfvar so the stack can reference it from `aws_lambda_function.filename`.

Source: [actions/deploy-terraform/action.yml](../../actions/deploy-terraform/action.yml).

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
| `lambda-zip-path` | yes | — | Absolute path to the artifact. Passed as `-var=lambda_zip_path=...`. |

## Outputs

None.

## Caller requirements

Job must declare `permissions: id-token: write`. The Terraform stack must declare `variable "lambda_zip_path"`.

## Example usage

[cd-lambda-python.yml](../../.github/workflows/cd-lambda-python.yml).
