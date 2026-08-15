# Dependencies

Sentinel dependency execution uses a private, owner-reviewed trusted registry. A plugin repository may request a dependency by stable registry ID, but it does not choose the source repository, version, commit, workflow run, artifact ID, download URL, checksum, plugin identity, or transitive closure.

Example manifest fragment:

```yaml
dependencies:
  - id: worldguard
    kind: hard
```

If the trusted registry says `worldguard` requires `worldedit`, Sentinel resolves the reviewed dependency-first closure. Do not duplicate transitive dependencies merely to bypass registry policy.

## Dependency source is not execution authorization

A repository used only to produce a trusted dependency artifact does not become a Sentinel execution target. Execution repository tokens and dependency-source tokens remain separate, short-lived, and narrowly scoped.

## Changing dependency trust

Adding a dependency, changing its exact provenance, refreshing an expired lock, or changing trusted closure is a Sentinel-owner-reviewed privilege/trust change. Repository managers cannot perform this through `.enthusia-test.yml` or a command.

If a lock expires or becomes inaccessible, Sentinel fails closed until the operator reproduces, reviews, relocks, deploys, and re-verifies the intended dependency. Do not substitute `latest` or a direct URL.
