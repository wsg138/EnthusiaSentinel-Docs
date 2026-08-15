# Enthusia Sentinel

Sentinel is a shared, GitHub-driven staging service for testing Minecraft plugins against controlled disposable Paper environments. This repository is the public human-facing documentation bundle; it contains no control-plane credentials or trusted production policy.

## I want to…

- **Test my plugin:** start with [Getting started](docs/getting-started.md), then [Using Sentinel](docs/using-sentinel.md).
- **Add a repository:** follow [Project onboarding](docs/project-onboarding.md).
- **Run a test:** use the exact commands in [Using Sentinel](docs/using-sentinel.md) and choose from [Profiles](docs/profiles.md).
- **Understand a failure:** use [Troubleshooting](docs/troubleshooting.md), then escalate only when needed.
- **Remove my repository:** follow [Disconnecting](docs/disconnecting.md).
- **Understand ownership:** read [User and repository ownership](docs/user-and-repository-ownership.md).
- **Understand artifacts or dependencies:** read [Artifacts](docs/artifacts.md) and [Dependencies](docs/dependencies.md).
- **Understand the trust boundary:** read [Security model](docs/security-model.md).
- **I am a Sentinel operator:** use [Operator escalation](docs/operator-escalation.md); private implementation runbooks remain in the trusted control repository.

## What Sentinel is

Sentinel accepts only repositories that have been deliberately onboarded by the Sentinel owner. For an authorized repository it binds work to an immutable repository identity, exact commit SHA, approved profile, validated `.enthusia-test.yml`, and a successful GitHub Actions artifact for that same SHA. Test execution is disposable and results are returned to GitHub.

## What Sentinel is not

Sentinel is not a general CI runner, shell service, remote server account, production Minecraft server, arbitrary artifact downloader, or permission shortcut. Installing the GitHub App does **not** authorize a repository for execution. A repository still needs reviewed Sentinel onboarding and a profile allowlist.

## Security and control

The existing **Enthusia Sentinel** GitHub App may be installed independently on multiple GitHub accounts or organizations. Each onboarded repository maps to exactly one trusted installation. Short-lived installation tokens are narrowed to the repositories Sentinel is actively serving for that installation. Repository managers can use only their own repository scope; they cannot manage another tenant or the private control plane.

Privilege increases—new repository enrollment, more profiles, manager changes, dependency trust, or re-enrollment after disconnect—require Sentinel-owner review. A legitimate repository manager can reduce access by disconnecting their repository without control-plane access and can separately change or remove the GitHub App installation/repository selection in GitHub.

## Copy-paste AI prompts

### Prepare a plugin repository

> Prepare this Minecraft plugin repository for Enthusia Sentinel. Inspect the real build, plugin metadata, Java/Paper versions, deployable JAR, dependencies, config/database/restart behavior, and existing CI. Add a safe `.enthusia-test.yml`, publish a dedicated exact-SHA Actions artifact from the existing build, and document only the Sentinel profiles the plugin actually needs. Do not add credentials, arbitrary URLs, shell execution, host paths, resource controls, or mutable/latest artifact selection.

### Onboard a repository

> Help me onboard this repository to Enthusia Sentinel. Verify its immutable GitHub repository identity and owner, confirm the existing Enthusia Sentinel GitHub App is installed on the owning account/organization with this repository visible, review the repository-side Sentinel manifest/artifact setup, choose the minimum automatic/manual profile set, and prepare the information the Sentinel owner needs for reviewed control-plane authorization. Do not create a new GitHub App or PAT.

### Troubleshoot a failed run

> Troubleshoot this Enthusia Sentinel result using the PR comment/check, exact SHA, profile, queue state, artifact workflow, `.enthusia-test.yml`, and bounded result code. Distinguish queue/resource deferral from test failure. Do not suggest bypassing exact-SHA, provenance, manager authorization, App installation scope, dependency locks, or isolation controls.

### Disconnect a repository

> Help me safely disconnect this repository from Enthusia Sentinel. Confirm I am a legitimate manager, cancel only eligible jobs belonging to this repository, issue the exact repository disconnect command on an open same-repository non-draft PR, verify Sentinel reports the repository disconnected, then show how to reduce or revoke the existing Enthusia Sentinel GitHub App access from my GitHub account/organization. Do not request control-repository access or delete another repository’s jobs.
