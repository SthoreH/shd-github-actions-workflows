# parse-config

Reads the consumer's `.pipeline.yml`, merges global blocks with the selected environment's section, and emits a flattened JSON map plus the list of files declared for token substitution. Used at the top of any pipeline that needs config-driven behavior.

Source: [actions/parse-config/action.yml](../../actions/parse-config/action.yml).

## Inputs

| Input | Required | Default | Description |
|---|---|---|---|
| `environment` | yes | — | Which `environments.<env>` block to merge in. |
| `config_file` | no | `.pipeline.yml` | Path to the config file relative to the repo root. |

## Outputs

| Output | Description |
|---|---|
| `config` | JSON string with flattened keys (`pipe_<section>_<key>`). |
| `files_to_replace` | Space-separated list from `environments.files-to-replace`. Consumed by [replace-tokens](replace-tokens.md). |

See [conventions](../conventions.md) for the full schema and key flattening rules.

## Example usage

[ci-lambda-python.yml](../../.github/workflows/ci-lambda-python.yml).
