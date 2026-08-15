# Enthusia Sentinel Documentation

**Enthusia Sentinel is the shared staging and runtime-testing system used to test Minecraft plugins before they are merged or released.**

It connects to approved GitHub repositories, takes the plugin build for the **exact commit being reviewed**, starts it in a disposable Paper server on trusted staging hardware, runs the approved test profile, and reports the result back to GitHub.

This repository is the public documentation for using Sentinel. It does **not** contain the private Sentinel control plane, credentials, Pi access, production policy, or server secrets.

## Who this is for

Use these docs if you:

- maintain a Minecraft plugin that should be tested through Enthusia Sentinel;
- need to connect a new GitHub repository;
- want to run or understand Sentinel tests on a pull request;
- manage a repository that is already connected;
- need to disconnect your repository from Sentinel.

You do **not** need SSH access to the staging Pi or access to the private Sentinel repository to use Sentinel normally.

## What Sentinel does

For an approved repository, Sentinel can:

1. identify the exact GitHub repository and commit SHA under test;
2. verify the repository's `.enthusia-test.yml` configuration;
3. find the successful GitHub Actions artifact built for that exact SHA;
4. verify the artifact and plugin identity before execution;
5. start a clean disposable Paper environment;
6. run the repository's approved test profile;
7. clean up the test environment; and
8. report the result back to the pull request/checks.

Depending on the repository, approved profiles can test things such as basic startup, restart behavior, configuration, databases, dependencies, Java clients, Bedrock clients, and broader integration behavior. See [Profiles](docs/profiles.md) for the supported profile types.

## What Sentinel does not do

Sentinel is **not**:

- a production Minecraft server;
- a general-purpose shell or remote-access service;
- a replacement for normal build/test CI;
- permission to run arbitrary code on the staging host;
- automatically enabled just because the GitHub App is installed.

Every repository must be deliberately onboarded and given an explicit profile allowlist by the Sentinel owner.

## New project? Start here

If you want to connect another plugin repository, follow this order:

1. Read [Getting started](docs/getting-started.md).
2. Prepare your build artifact and `.enthusia-test.yml`.
3. Install the existing **Enthusia Sentinel** GitHub App on the account or organization that owns the repository and make the intended repository visible to it.
4. Follow [Project onboarding](docs/project-onboarding.md) so the Sentinel owner can review and authorize the repository.
5. After onboarding, run the first test from an open, non-draft pull request using one of the exact commands in [Using Sentinel](docs/using-sentinel.md).

Installing the App alone does **not** give Sentinel execution permission. The repository must also be added to Sentinel's trusted configuration.

## Already connected? Common tasks

- **Run or check a test:** [Using Sentinel](docs/using-sentinel.md)
- **Choose or understand a profile:** [Profiles](docs/profiles.md)
- **Understand a failure:** [Troubleshooting](docs/troubleshooting.md)
- **Understand build artifacts:** [Artifacts](docs/artifacts.md)
- **Use trusted plugin dependencies:** [Dependencies](docs/dependencies.md)
- **Understand who can manage a repository:** [User and repository ownership](docs/user-and-repository-ownership.md)
- **Disconnect your repository:** [Disconnecting](docs/disconnecting.md)

## How repository access works

Sentinel uses the existing **Enthusia Sentinel GitHub App**. The same App can be installed on more than one GitHub account or organization.

A connected repository is tied to:

- its immutable GitHub repository identity;
- one specific GitHub App installation;
- its approved Sentinel profiles; and
- any explicitly assigned repository managers.

Repository managers only receive authority for repositories assigned to them. Managing one repository does not grant access to another repository or to the private Sentinel control plane.

New repositories, additional profiles, manager changes, trusted dependencies, and reconnecting a previously disconnected repository require Sentinel-owner review.

## Removing your repository

Repository owners are not locked into Sentinel.

If you are an authorized manager for the repository, you can reduce Sentinel access with:

```text
@enthusia-sentinel disconnect repository
```

See [Disconnecting](docs/disconnecting.md) for the required pull-request context and what the command does.

The GitHub account or organization owner can also independently remove that repository from the Sentinel App installation or uninstall the App entirely.

## Documentation

### Setup and everyday use

- [Getting started](docs/getting-started.md)
- [Project onboarding](docs/project-onboarding.md)
- [Using Sentinel](docs/using-sentinel.md)
- [Profiles](docs/profiles.md)
- [Troubleshooting](docs/troubleshooting.md)

### Repository configuration

- [Artifacts](docs/artifacts.md)
- [Dependencies](docs/dependencies.md)
- [Maven example](examples/maven/pom.xml)
- [Gradle example](examples/gradle/build.gradle.kts)
- [Minimal manifest example](examples/manifests/minimal.yml)
- [Dependency manifest example](examples/manifests/dependencies-manual.yml)

### Access and security

- [User and repository ownership](docs/user-and-repository-ownership.md)
- [Disconnecting](docs/disconnecting.md)
- [Security model](docs/security-model.md)
- [Operator escalation](docs/operator-escalation.md)

## Need help?

Start with [Troubleshooting](docs/troubleshooting.md). If the problem involves repository authorization, GitHub App installation mapping, manager access, trusted dependencies, or the Sentinel service itself, use the escalation path in [Operator escalation](docs/operator-escalation.md).
