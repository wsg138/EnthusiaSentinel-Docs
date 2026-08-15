# Troubleshooting

Start with the GitHub check/comment for the exact repository, PR, SHA, and profile. Sentinel intentionally returns bounded result codes rather than private host details.

## Queued or resource-gated

`queued` is not a plugin failure. Sentinel serializes heavy work and may defer execution when the shared host is below trusted memory/disk limits, too hot, at client capacity, or already running another heavy job. Do not repost commands merely because a valid job is waiting.

## `PROFILE_NOT_ALLOWED`

The requested profile is outside the repository’s reviewed Sentinel allowlist. A repository manifest cannot grant itself more capability. Ask the Sentinel owner only if the project genuinely needs the extra profile.

## Authorization failures

If Sentinel says the commenter/requester is not authorized or not a repository manager, verify the GitHub account you used and ask the Sentinel owner to verify the immutable numeric user ID and repository-manager mapping. Being authorized for another repository does not carry over.

## Manifest failures

Validate that `.enthusia-test.yml` is present at the exact tested SHA and matches the documented schema. Do not add credentials, URLs, host paths, shell, resource limits, or dependency provenance to make validation pass.

## Artifact failures

Confirm a successful GitHub Actions workflow exists for the exact tested SHA, the uploaded artifact name matches the manifest, and the expected JAR path exists inside it. A branch-latest or artifact from a different SHA is not valid evidence.

## App installation/access failures

Confirm the existing Enthusia Sentinel App is still installed on the repository owner account/organization and the repository is visible to that installation. Do not create a new App or PAT. If the repository was intentionally disconnected, installation visibility alone will not reconnect it.

## Dependency failures

The repository may request only trusted dependency IDs. Version/source/run/artifact/checksum provenance is controlled by Sentinel’s private reviewed dependency registry. If a trusted lock is expired or inaccessible, escalate; do not substitute `latest` or a direct download URL.

## Restart/config/database/client failures

Read the profile-specific result code and compare the plugin behavior with [Profiles](profiles.md). Sentinel tests a disposable environment; it does not expose production server data or credentials.

## When to escalate

Escalate when the problem appears to be installation mapping, trusted policy, dependency locks, Sentinel service availability, or a reproducible control-plane defect. Include repository, PR, exact SHA, command/profile, GitHub check/comment, and bounded result code. Never send App private keys, tokens, database credentials, SSH material, or production server data.
