# Artifacts

Sentinel executes a deployable plugin JAR from a successful GitHub Actions artifact for the **exact commit SHA** under test.

## Required contract

Your `.enthusia-test.yml` supplies only the stable Actions artifact name and normalized JAR path inside that artifact. Sentinel independently verifies immutable repository identity, workflow run SHA and success, artifact identity, archive limits, expected JAR path, and content provenance before execution.

## Do not use

Do not use `latest` or branch-latest artifacts, release URLs, third-party file hosts, local host files, credentials, mutable download discovery, or shell-based artifact fetching.

## Maven/Gradle publication

Use the repository's existing build and add a dedicated `actions/upload-artifact` step for the final plugin JAR. Keep Actions pinned according to the repository's normal security policy. The examples here show repository-side shape only.

## Why exact SHA matters

If a PR moves from SHA A to SHA B, an artifact from A cannot prove B. Sentinel binds each admitted job to one immutable SHA and rejects mismatched workflow/artifact evidence.
