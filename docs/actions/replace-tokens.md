# replace-tokens

Substitutes `${token}` placeholders in declared files using a JSON map of values. Run after [parse-config](parse-config.md) and before packaging in CD, so source files carry env-specific values into the artifact.

Source: [actions/replace-tokens/action.yml](../../actions/replace-tokens/action.yml).

## Inputs

| Input | Required | Description |
|---|---|---|
| `files` | yes | Space-separated list of file paths to process. Typically `${{ steps.config-parser.outputs.files_to_replace }}`. |
| `vars` | yes | JSON string of key/value substitutions. Typically `${{ steps.config-parser.outputs.config }}`. |

## Outputs

None.

## Example usage

[cd-lambda-python.yml](../../.github/workflows/cd-lambda-python.yml).
