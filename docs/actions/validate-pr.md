# validate-pr

Enforces three things on a pull request: branch flow (`feature/* → dev → main`), Conventional Commits in the title (configurable), and a non-empty description (configurable). Use it as the first step of any consumer's PR-triggered workflow.

Source: [actions/validate-pr/action.yml](../../actions/validate-pr/action.yml).

## Inputs

| Input | Required | Default | Description |
|---|---|---|---|
| `github-token` | yes | — | Token used to read the PR via the API. Pass `secrets.GITHUB_TOKEN`. |
| `validate-title` | no | `'true'` | Toggle Conventional Commits title validation. |
| `validate-description` | no | `'true'` | Toggle PR-description-non-empty validation. |

## Outputs

None.

## Example usage

[app-aws-lbd-products-service/.github/workflows/ci-prod.yml](../../../../app/app-aws-lbd-products-service/.github/workflows/ci-prod.yml).
