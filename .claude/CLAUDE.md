# Repo: shd-github-actions-workflows

Reusable GitHub Actions workflows + composite actions consumed across SthoreH product repos. Treat any change here as a public API change — consumers pin to tags.

## Where things live

- [.github/workflows/](../.github/workflows/) — reusable workflows (`workflow_call`).
- [actions/](../actions/) — composite actions.
- [docs/](../docs/) — one markdown per piece + [docs/conventions.md](../docs/conventions.md). Update on every change.

## Authoring rules

- **Naming** — jobs and steps follow **Action + Target** ("Validate Terraform", "Deploy Lambda"). Job IDs (dictionary keys) stay stable across renames.
- **Pinning third-party actions** — major only (`actions/checkout@v4`, never `@v4.1.0`, never `@main`).
- **Comments** — English, only on non-obvious behavior (OIDC requirements, hidden contracts, conventions). No comments on self-explanatory steps.
- **Backend convention** — `tf-backend-key` is `{repo-name}/terraform.tfstate`. Env separation comes from per-env `vars.TF_STATE_BUCKET`, never the key.
- **OIDC** — composite actions calling `aws-actions/configure-aws-credentials` assume the caller job declared `permissions: id-token: write`. Document this in the action's `docs/` page.
- **Docs are part of the change** — when adding/renaming an input or a piece, update its `docs/` file in the same commit.

## Versioning

semantic-release tags on merges to `main`. Conventional Commits in the PR title drive the bump. No breaking changes without a major bump (renaming or removing an input is breaking; adding an input with a default is not).
