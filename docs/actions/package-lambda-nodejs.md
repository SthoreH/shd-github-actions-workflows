# package-lambda-nodejs

Builds a Lambda-compatible `.zip` for Node.js: runs `pnpm install --frozen-lockfile`, copies the full working-directory structure (excluding `node_modules`) to a staging directory, installs production dependencies with a flat `node_modules` layout (`--shamefully-hoist`), then zips the result. Run during CD between [replace-tokens](replace-tokens.md) and [deploy-terraform](deploy-terraform.md).

Source: [actions/package-lambda-nodejs/action.yml](../../actions/package-lambda-nodejs/action.yml).

## Inputs

| Input | Required | Default | Description |
|---|---|---|---|
| `nodejs-version` | yes | — | Node.js major version (e.g. `22`). Drives `actions/setup-node`. |
| `working-directory` | yes | — | Source root containing `package.json` and `pnpm-lock.yaml` (e.g. `app`). |
| `output-path` | no | `${{ github.workspace }}/dist/lambda.zip` | Where to write the final zip. |
| `pnpm-version` | no | `9` | pnpm major version installed by `pnpm/action-setup`. |

## Outputs

| Output | Description |
|---|---|
| `zip-path` | Absolute path to the produced `.zip`. The file mirrors the working-directory structure with a flat `node_modules` at its root. |

## Package layout

The zip contains all files from `working-directory` (directory structure preserved) plus production `node_modules` installed with `--shamefully-hoist`. The flat `node_modules` layout is required because Lambda's `require()` does not resolve pnpm's symlinked virtual store.

## Example usage

[cd-lambda-nodejs.yml](../../.github/workflows/cd-lambda-nodejs.yml).
