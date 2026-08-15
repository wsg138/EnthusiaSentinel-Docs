# User and repository ownership

Sentinel separates four kinds of authority:

1. **GitHub App installation ownership.** A GitHub user or organization controls whether the existing Enthusia Sentinel App is installed and which repositories that installation can see.
2. **Sentinel execution authorization.** The private control plane maps immutable repository IDs/names to exactly one trusted App installation and defines the maximum profile/automation surface.
3. **Repository management.** Trusted numeric GitHub user IDs are bound to specific repositories. Non-admin maintainers cannot use their global Sentinel role on repositories they do not manage.
4. **Sentinel operator authority.** The Sentinel owner controls trusted policy, dependency registry, deployment, App credentials, host/runtime configuration, and privilege increases.

## What a repository manager can do independently

For a repository they legitimately manage and while it is connected, a manager can use the exact commands allowed by their role and repository policy, inspect Sentinel status/results for current repository work, cancel eligible jobs in that repository scope, and disconnect the repository. They can also independently change repository selection or uninstall the GitHub App from the GitHub account/organization they administer.

## What requires Sentinel-owner approval

- initial repository enrollment;
- mapping a repository to an App installation;
- adding/changing repository managers;
- granting additional profiles or automatic transitions;
- enabling fork testing;
- trusting or changing dependency provenance;
- re-enrolling a disconnected repository;
- any control-plane/runtime/security-policy change.

## Cross-tenant isolation

A manager binding for repository A does not authorize repository B. GitHub App visibility is also not enough: even if an installation can see many repositories, Sentinel scopes short-lived tokens to the connected trusted repositories assigned to that installation and still performs repository/user/profile/exact-SHA admission.

The private control-plane repository is not a tenant collaboration surface. External maintainers do not need collaborator access to it.
