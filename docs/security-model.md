# Security model

Sentinel is designed as a shared least-privilege staging service. Normal users interact through GitHub; they do not receive shell access or control-plane repository access.

## Independent gates

A run requires all applicable gates:

- repository appears in reviewed Sentinel execution policy by immutable numeric ID plus canonical name;
- repository maps to exactly one reviewed installation of the existing Enthusia Sentinel GitHub App;
- repository is not disconnected for its current connection epoch;
- requester/commenter has an authorized global capability **and** is a manager of that repository (unless they are the Sentinel admin);
- profile is allowed for that repository;
- PR/merge state and fork rules are satisfied;
- commit SHA is exact and immutable;
- `.enthusia-test.yml` validates under the bounded schema;
- target artifact comes from a successful exact-SHA GitHub Actions run;
- resource and one-heavy-job gates permit execution.

## Multiple installations, one App

Sentinel uses one GitHub App identity with independent installations on different GitHub users or organizations. Each installation token is short-lived and created only for the connected repositories assigned to that installation. A token for one installation is never used as authority for another installation.

Installing the App on all repositories in an account does not authorize all of those repositories in Sentinel.

## Isolation

Plugin tests run in disposable rootless environments with bounded resources and loopback-only synthetic client networking where applicable. Repository manifests cannot select host mounts, arbitrary network targets, credentials, shell, trusted executable paths, or resource limits.

## Credentials and private topology

Public documentation does not contain App private keys, installation tokens/JWTs, host credentials, SSH material, database credentials, production Minecraft data, private queue contents, or trusted control-plane topology. External documentation contributors cannot execute trusted self-hosted runner code through this documentation bundle.

## Privilege direction

Privilege increases require Sentinel-owner review. A legitimate repository manager can reduce privilege by cancelling their own eligible jobs, disconnecting their repository, and changing/uninstalling the App installation in GitHub where they administer it. Disconnect cannot self-reverse; re-enrollment requires a new reviewed connection epoch.
