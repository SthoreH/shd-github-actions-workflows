# package-lambda-python

Builds a Lambda-compatible `.zip`: installs runtime dependencies into a build directory, copies the source on top, then zips the bundle. Run during CD between [replace-tokens](replace-tokens.md) and [deploy-terraform](deploy-terraform.md).

Source: [actions/package-lambda-python/action.yml](../../actions/package-lambda-python/action.yml).

## Inputs

| Input | Required | Default | Description |
|---|---|---|---|
| `python-version` | yes | — | Used by `actions/setup-python`. |
| `working-directory` | yes | — | Source root containing app code and the requirements file (e.g. `app/src`). |
| `requirements` | yes | — | Requirements file name relative to `working-directory`. |
| `output-path` | no | `${{ github.workspace }}/dist/lambda.zip` | Where to write the final zip. |

## Outputs

| Output | Description |
|---|---|
| `zip-path` | Absolute path to the produced `.zip`. Pass to [deploy-terraform](deploy-terraform.md) as `lambda-zip-path`. |

## Example usage

[cd-lambda-python.yml](../../.github/workflows/cd-lambda-python.yml).
