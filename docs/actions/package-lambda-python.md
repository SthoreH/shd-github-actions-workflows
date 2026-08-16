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
| `architecture` | no | `""` | Target Lambda architecture (`x86_64` or `arm64`). Runners are x86_64; for `arm64` the install fetches `manylinux2014_aarch64` wheels via `--platform`/`--only-binary=:all:` instead of building for the host. Every dependency must ship a wheel for that platform. Any value other than exactly `arm64` behaves like today. See "Architecture resolution" below for what an empty value does. |

## Architecture resolution

The `architecture` input defaults to an empty string, not `x86_64`, so the action can fall back to the consumer's `.pipeline.yml` when the caller doesn't pass it explicitly. Resolution order, evaluated at build time by the "Build package" step:

1. **Input** — if `architecture` is non-empty, use it as-is. `.pipeline.yml` is not consulted.
2. **`.pipeline.yml`** — if the input is empty, read `.runtime.architecture` from `${{ github.workspace }}/.pipeline.yml` (repo root) via `yq`. Used if present and non-null.
3. **Default (`x86_64`)** — if neither the input nor the file has a value (no file, no `runtime` block, no `architecture` key, or a null/empty value), fall back to `x86_64` — today's behavior, unconditionally safe even though the step runs under `set -euo pipefail`.

The resolved value and which source won are logged (`Resolved architecture: <value> (source: <input|.pipeline.yml|default>)`) so a surprising package (wrong wheels, import failure) is diagnosable straight from the run log.

This fallback is what lets repos still pinned to an older tag of `cd-lambda-python.yml`/`ci-lambda-python.yml` (from before the `architecture` input and its `pipe_runtime_architecture` plumbing existed) get correct `arm64` wheels for a Lambda that declares `architecture: arm64` in its own `.pipeline.yml`, without bumping their pin. Callers that do wire the input through the reusable workflows (current `@main`) get the same result via the explicit path — the file read is skipped entirely in that case.

## Outputs

| Output | Description |
|---|---|
| `zip-path` | Absolute path to the produced `.zip`. Pass to [deploy-terraform](deploy-terraform.md) as `lambda-zip-path`. |

## Package layout

The zip contains dependencies (from `pip install -t`) plus all source files from `working-directory` (directory structure preserved, requirements file excluded). Source files are copied on top of dependencies so they take precedence in case of name collisions.

## Example usage

[cd-lambda-python.yml](../../.github/workflows/cd-lambda-python.yml).
