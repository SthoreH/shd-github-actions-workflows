# package-lambda-nodejs

Builds a Lambda-compatible `.zip` for Node.js (TypeScript or JavaScript): runs `pnpm install --frozen-lockfile`, bundles the entry file with esbuild as a single minified `index.js`, then zips it. AWS SDK v3 is externalized (provided by the `nodejs22.x` runtime). Run during CD between [replace-tokens](replace-tokens.md) and [deploy-terraform](deploy-terraform.md).

Source: [actions/package-lambda-nodejs/action.yml](../../actions/package-lambda-nodejs/action.yml).

## Inputs

| Input | Required | Default | Description |
|---|---|---|---|
| `nodejs-version` | yes | — | Node.js major version (e.g. `22`). Drives `actions/setup-node` and the esbuild `--target=node<N>`. |
| `working-directory` | yes | — | Source root containing `package.json` and `pnpm-lock.yaml` (e.g. `app`). |
| `entry-file` | yes | — | Entry file for esbuild, relative to `working-directory` (e.g. `src/index.ts`). |
| `output-path` | no | `${{ github.workspace }}/dist/lambda.zip` | Where to write the final zip. |
| `pnpm-version` | no | `9` | pnpm major version installed by `pnpm/action-setup`. |

## Outputs

| Output | Description |
|---|---|
| `zip-path` | Absolute path to the produced `.zip`. The file contains a single bundled `index.js`. |

## Bundle behavior

- `--bundle --platform=node --target=node<NODEJS_VERSION>`: produces a single self-contained file.
- `--external:@aws-sdk/*`: AWS SDK v3 modules are not bundled — they come from the Lambda runtime, keeping the artifact small.
- `--minify`: minified for cold-start performance.

If your code depends on packages outside of `@aws-sdk/*` that should NOT be bundled (e.g. native binaries), expose the action through this layer or fork — keep the bundling defaults aligned across the org.

## Example usage

[cd-lambda-nodejs.yml](../../.github/workflows/cd-lambda-nodejs.yml).
