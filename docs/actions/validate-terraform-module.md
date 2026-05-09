# validate-terraform-module

Lightweight Terraform validation (fmt + init without backend + validate). Intended for **module** repos that don't have a backend or environments — just verify the HCL is well-formed.

Source: [actions/validate-terraform-module/action.yml](../../actions/validate-terraform-module/action.yml).

## Inputs

| Input | Required | Default | Description |
|---|---|---|---|
| `terraform_version` | no | `1.14.8` | Terraform CLI version. (Note: snake_case; sibling [validate-terraform](validate-terraform.md) uses kebab-case — known inconsistency.) |

## Outputs

None.

## When to use

CI of a Terraform module repo (e.g. `shd-terraform-aws-lambda`). For consumer Lambda repos, use [validate-terraform](validate-terraform.md) instead.
