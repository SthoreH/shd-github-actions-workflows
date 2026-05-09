# shd-github-actions-workflows

Shared reusable workflows and composite actions for SthoreH repositories. Pipelines in product repos delegate to the pieces here so CI/CD is consistent across the org.

## What's here

- [.github/workflows/](.github/workflows/) — reusable workflows that consumer repos call via `uses:`.
- [actions/](actions/) — composite actions that workflows (or consumers) embed via `uses:` at the step level.
- [docs/](docs/) — per-piece documentation and shared conventions.

## Versioning

Consumers pin pieces to a published tag (e.g. `@v1.4.0`), never `@main`. Tags are produced by semantic-release on merges to `main`. Breaking changes bump the major; new inputs or new pieces bump the minor.

## Quick start for a new consumer repo

1. Add a [.pipeline.yml](docs/conventions.md) at the repo root describing your runtime, infra path, deploy paths, tests, and per-environment settings.
2. Configure GitHub Environments (`dev`, `prod`) with `vars.AWS_ROLE_ARN` and `vars.TF_STATE_BUCKET`. Set up the IAM role's OIDC trust for your repo. Details in [docs/conventions.md](docs/conventions.md).
3. Add caller workflows that delegate to the reusable workflows here. A real example lives at [app-aws-lbd-products-service/.github/workflows/](../../app/app-aws-lbd-products-service/.github/workflows/).

## Index

### Reusable workflows

| Workflow | Purpose |
|---|---|
| [ci-lambda-python](docs/workflows/ci-lambda-python.md) | Validates a Python Lambda repo (lint, tests, terraform fmt + validate + plan). |
| [cd-lambda-python](docs/workflows/cd-lambda-python.md) | Packages a Python Lambda and applies Terraform. Supports rollback via the `ref` input. |

### Composite actions

| Action | Purpose |
|---|---|
| [parse-config](docs/actions/parse-config.md) | Reads `.pipeline.yml`, merges environment-specific values, emits flattened JSON + token-replacement file list. |
| [replace-tokens](docs/actions/replace-tokens.md) | Substitutes `${token}` placeholders in declared files. |
| [validate-pr](docs/actions/validate-pr.md) | Enforces PR title (Conventional Commits), description, and branch flow rules. |
| [validate-terraform](docs/actions/validate-terraform.md) | Runs terraform fmt + init + validate + plan against an environment. |
| [validate-terraform-module](docs/actions/validate-terraform-module.md) | Lightweight validation (fmt + validate, no backend) for terraform module repos. |
| [package-lambda-python](docs/actions/package-lambda-python.md) | Builds a Lambda-compatible `.zip` (deps + source) for a Python project. |
| [deploy-terraform](docs/actions/deploy-terraform.md) | Runs terraform init + apply, passing the lambda artifact as a tfvar. |
| [destroy-terraform](docs/actions/destroy-terraform.md) | Runs terraform init + destroy. Generic; not lambda-specific. |

## Conventions

Cross-cutting rules every piece relies on (`.pipeline.yml` schema, environment vars, OIDC trust, terraform state key, permissions baseline, tagging) are documented in [docs/conventions.md](docs/conventions.md). Read this first if you're authoring or reviewing pipeline changes.
