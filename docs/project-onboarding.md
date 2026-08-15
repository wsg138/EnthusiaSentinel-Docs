# Project onboarding

Repository onboarding has a repository-owned part and a Sentinel-owner-reviewed part. External maintainers do **not** need access to the private control-plane repository.

## 1. Install the existing GitHub App

Install **Enthusia Sentinel** on the GitHub user or organization that owns the repository. Choose the repository visibility appropriate for your account. You may later change the selection or uninstall it yourself in GitHub.

Do not create a second Sentinel App and do not provide a personal access token.

## 2. Prepare the repository

Confirm from live source:

- canonical `OWNER/REPOSITORY`;
- immutable numeric GitHub repository ID;
- Java/Paper versions and plugin main class;
- Maven/Gradle build and real deployable JAR;
- hard/soft runtime dependencies;
- restart/reload/config/database/client behavior worth testing.

Add or reconcile:

- `.enthusia-test.yml`;
- exact-SHA Actions artifact publication;
- repository-local Sentinel documentation if useful.

Use `examples/manifests/` and the Maven/Gradle examples in this repository.

## 3. Choose automatic or manual-only behavior

**Automatic** repositories may run owner-approved profiles on PR lifecycle transitions such as opened, ready, reviewable-head changes, and merged commits.

**Manual-only** repositories create no lifecycle jobs and run only explicit allowed commands. This is appropriate when a plugin needs a narrow or expensive profile such as `dependencies` only.

The Sentinel owner chooses the smallest reviewed profile surface that matches the project. `dependencies` is manual-only.

## 4. Provide onboarding facts for review

Send the Sentinel operator:

- immutable repository ID and canonical full name;
- GitHub account/organization that owns it;
- confirmation that the existing App is installed and the repository is visible;
- immutable GitHub user IDs/logins for legitimate repository managers;
- requested manual profiles;
- requested automatic transitions/profiles, if any;
- whether fork startup testing is needed;
- dependency IDs needed from the trusted registry;
- link to the repository-side onboarding PR.

The operator independently verifies these facts. A mutable login/name alone is not sufficient authorization.

## 5. Owner-reviewed control-plane enrollment

The Sentinel owner reviews and publishes trusted configuration mapping the repository to exactly one GitHub App installation identity and one or more repository managers. This is a privilege increase and is never self-service.

The control plane also defines the maximum profile set and automatic/manual behavior. Repository configuration cannot broaden it.

## 6. Acceptance

After the reviewed control-plane change is deployed, freeze an open non-draft same-repository PR head with a successful exact-SHA artifact and run an allowed command. Record the PR/head, artifact workflow, Sentinel result, and profile-specific terminal code.

## Re-enrollment after disconnect

A disconnected repository is not re-enabled by reinstalling the App or reposting a command. Re-enrollment requires a fresh owner review and a new trusted connection epoch so an old repository-side action cannot restore privilege.
