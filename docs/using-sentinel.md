# Using Sentinel

Sentinel commands are exact, standalone GitHub pull-request comments. Normal commands require an open, non-draft, same-repository PR and a commenter who is authorized both globally for the requested role and as a manager of that repository. The repository must still be connected and the requested profile must be allowed by trusted policy.

## Exact commands

```text
@enthusia-sentinel status
@enthusia-sentinel test startup
@enthusia-sentinel test restart
@enthusia-sentinel test restart-config
@enthusia-sentinel test reload-config
@enthusia-sentinel test database
@enthusia-sentinel test dependencies
@enthusia-sentinel test java-client
@enthusia-sentinel test java-interaction
@enthusia-sentinel test bedrock-client
@enthusia-sentinel test full
@enthusia-sentinel test post-merge
@enthusia-sentinel cancel
@enthusia-sentinel approve-test startup
@enthusia-sentinel disconnect repository
```

No alternate spelling, extra prose, multiline form, prefix, suffix, or unapproved profile is accepted.

`test post-merge` is recognized but does not manually enqueue from an open PR; actual post-merge work is bound to GitHub’s confirmed merge commit by automatic orchestration.

`approve-test startup` is the explicit fork-startup path and works only where fork testing is enabled by trusted repository policy. Fork execution never grants general fork access.

## Status and results

`@enthusia-sentinel status` reports durable Sentinel state for the current repository/PR/exact head. Automatic and manual jobs for that exact scope can appear. Results are also published through GitHub checks/comments with bounded evidence.

Typical states:

- `queued`: admitted but waiting for the one-heavy lane or a resource gate;
- `running`: actively executing;
- `passed`: the profile reached its required terminal success;
- `failed`: a validation/runtime/security condition failed;
- `cancelled`: an eligible job received a scoped cancellation;
- `superseded`: a safe queued automatic job was replaced by newer exact-head work.

A queue position or resource deferral does not mean the plugin failed.

## Exact-SHA behavior

Sentinel binds a job to one immutable commit SHA. The manifest is fetched at that SHA. The target JAR must come from a successful GitHub Actions workflow whose `head_sha` is the same SHA. If the PR head moves, the old evidence does not silently become evidence for the new head.

## Cancel

```text
@enthusia-sentinel cancel
```

This can cancel eligible queued/running jobs linked to the current repository, PR, and exact head. It refuses shared scope and cannot cancel another repository’s work.

## Disconnect

```text
@enthusia-sentinel disconnect repository
```

This is a reduction-only action for a legitimate repository manager. It records a durable disconnect for the current trusted enrollment epoch, requests cancellation only for active jobs belonging to that repository, and removes the repository from subsequent polling/token scope. Re-enrollment requires Sentinel-owner review and a new trusted connection epoch.

See [Disconnecting](disconnecting.md) before using it.
