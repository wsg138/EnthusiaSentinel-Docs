# Disconnecting

Disconnecting is intentionally easier than gaining access. It reduces Sentinel privilege for one repository and does not require control-plane owner intervention.

## Before disconnecting

Use `@enthusia-sentinel status` on your repository’s current open, non-draft, same-repository PR if you need to capture final job information. Decide whether active work should finish or be cancelled.

## Disconnect from Sentinel

Post this exact standalone comment on an open, non-draft, same-repository pull request:

```text
@enthusia-sentinel disconnect repository
```

You must be a trusted manager of that repository and have the existing cancel capability. Sentinel records a durable disconnect for the repository’s current trusted connection epoch, requests cancellation for eligible queued/running jobs whose repository identity matches, reports the reduction, and removes the repository from later polling and installation-token scope.

The command cannot disconnect another repository, alter trusted dependency policy, change managers, change profiles, or modify the Sentinel control plane.

## Revoke or reduce the GitHub App installation yourself

The GitHub account or organization that installed **Enthusia Sentinel** remains in control of the GitHub-side installation. In GitHub settings, open the installed GitHub Apps area for that account/organization, select **Enthusia Sentinel**, then either remove this repository from the installation’s repository selection or uninstall the App entirely if that is what you want.

Changing GitHub installation visibility and Sentinel disconnect are separate controls. Doing either one reduces effective access; doing both is appropriate when you want a full offboarding from both layers.

## What remains after disconnect

Historical GitHub comments/checks and ordinary repository history may remain. Sentinel does not reinterpret old artifacts or old job records as current authorization. A disconnected repository does not receive new Sentinel polling/execution.

## Re-enrolling later

Re-enrollment is a privilege increase. Ask the Sentinel owner for a fresh review. The owner verifies the live repository, installation, managers, manifest/artifact setup, and profile scope and then publishes a new trusted connection epoch. Reinstalling the App alone does not reconnect Sentinel.
