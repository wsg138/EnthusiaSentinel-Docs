# Artifacts

Sentinel executes a deployable plugin JAR from a successful GitHub Actions artifact for the **exact commit SHA** under test.

## Required contract

Your `.enthusia-test.yml` supplies only the stable Actions artifact name and normalized JAR path inside that artifact. Sentinel independently verifies immutable repository identity, workflow run SHA and success, artifact identity, archive limits, expected JAR path, and content provenance before execution.

## Do not use for Sentinel executable inputs

Do not use `latest` or branch-latest artifacts, release URLs, third-party file hosts, local host files, credentials, mutable download discovery, or shell-based artifact fetching for a Sentinel executable plugin input. Sentinel executable admission remains bound to the exact successful Actions artifact declared by `.enthusia-test.yml`.

## Canonical Pi evidence is different

EnthusiaStaff canonical Pi staging has a separate evidence-retention contract. After the trusted private `Lincoln-PI-4` run has produced its **sanitized evidence directory**, `wsg138/EnthusiaStaff-Staging` stores that evidence as a private GitHub prerelease asset on every run rather than as a GitHub Actions artifact. The release tag is deterministically bound to the private workflow run ID and attempt, and the evidence ZIP name is bound to the exact EnthusiaStaff source SHA plus the same private run identity.

Those private release assets are **evidence output only**. They are never executable plugin inputs and do not weaken Sentinel's Actions-artifact admission rules. Raw credentials, database contents, and unsanitized runtime material remain prohibited from evidence releases.

## Maven/Gradle publication

For Sentinel executable inputs, use the repository's existing build and add a dedicated `actions/upload-artifact` step for the final plugin JAR. Keep Actions pinned according to the repository's normal security policy. The examples here show repository-side shape only.

## Why exact SHA matters

If a PR moves from SHA A to SHA B, an artifact from A cannot prove B. Sentinel binds each admitted job to one immutable SHA and rejects mismatched workflow/artifact evidence. Canonical Pi evidence releases follow the same principle: the retained evidence identity must remain bound to the exact source SHA and exact private run that generated it.
