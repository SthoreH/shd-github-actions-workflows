# package-lambda-python

Builds a Lambda-compatible `.zip`: installs runtime dependencies into a staging directory, copies the full working-directory structure on top (preserving subdirectories), then zips the result. Run during CD between [replace-tokens](replace-tokens.md) and [deploy-terraform](deploy-terraform.md).

Source: [actions/package-lambda-python/action.yml](../../actions/package-lambda-python/action.yml).

## Inputs

| Input | Required | Default | Description |
|---|---|---|---|
| `python-version` | yes | — | Used by `actions/setup-python`. |
| `working-directory` | yes | — | Source root containing app code and the requirements file (e.g. `app`). |
| `requirements` | yes | — | Requirements file name relative to `working-directory`. |
| `output-path` | no | `${{ github.workspace }}/dist/lambda.zip` | Where to write the final zip. |
| `architecture` | no | `x86_64` | Target Lambda architecture (`x86_64` or `arm64`). Runners are x86_64; for `arm64` the install fetches `manylinux2014_aarch64` wheels via `--platform`/`--only-binary=:all:` instead of building for the host. Every dependency must ship a wheel for that platform. Any value other than exactly `arm64` (including an empty string) behaves like today. |

## Outputs

| Output | Description |
|---|---|
| `zip-path` | Absolute path to the produced `.zip`. Pass to [deploy-terraform](deploy-terraform.md) as `lambda-zip-path`. |

## Package layout

The zip contains dependencies (from `pip install -t`) plus all source files from `working-directory` (directory structure preserved, requirements file excluded). Source files are copied on top of dependencies so they take precedence in case of name collisions.

## Example usage

[cd-lambda-python.yml](../../.github/workflows/cd-lambda-python.yml).
