# Getting started

## Before Sentinel can run your plugin

Your repository needs four things:

1. The existing **Enthusia Sentinel** GitHub App installed on the GitHub user or organization that owns the repository, with the repository visible to that installation.
2. A normal build that produces the real Paper plugin JAR.
3. A dedicated GitHub Actions artifact published by a successful workflow for the **exact commit SHA** being tested.
4. A reviewed `.enthusia-test.yml` describing the plugin, artifact name/path, supported profiles, and bounded test fixtures/actions.

Installing the App is necessary for private repositories but is not execution authorization. The Sentinel owner must separately review and add the repository’s immutable numeric ID, exact `owner/repository` identity, GitHub App installation mapping, repository managers, automatic/manual behavior, and profile allowlist.

## Repository-side preparation

### Maven

See `examples/maven/pom.xml`. Keep your normal Maven build; add an Actions upload step for the final deployable JAR. The manifest `artifact.jar_path` must match the path inside the uploaded artifact.

### Gradle

See `examples/gradle/build.gradle.kts`. Keep the project’s real Gradle build and upload the actual plugin JAR, not an intermediate or sources JAR.

### Manifest

Start from `examples/manifests/minimal.yml`. Every declared profile must be both supported by Sentinel and approved for your repository. Repository manifests cannot select credentials, host paths, shell commands, arbitrary URLs, resource budgets, or trusted dependency provenance.

## First test

For a manual run, use an **open, non-draft, same-repository pull request** whose current head has a successful matching artifact. Post one exact standalone command such as:

```text
@enthusia-sentinel test startup
```

Do not add explanatory text to the command comment. Sentinel rechecks repository identity, manager authorization, PR state, exact head SHA, manifest, profile policy, and artifact provenance before admission.

## What success looks like

Sentinel updates a GitHub status/check and command response with the exact SHA, job state, stage, bounded result code, and summary. A profile-specific terminal code confirms runtime success; examples include `PAPER_SMOKE_OK`, `PAPER_RESTART_OK`, and `PAPER_DEPENDENCIES_OK`.

`queued` is not a failure. Sentinel has one shared heavy execution lane and also enforces memory, disk, temperature, timeout, and client limits. A resource-gated job remains queued/deferred instead of overcommitting the staging host.

## Next

- Commands and results: [Using Sentinel](using-sentinel.md)
- Choosing profiles: [Profiles](profiles.md)
- Full onboarding process: [Project onboarding](project-onboarding.md)
- Failures: [Troubleshooting](troubleshooting.md)
