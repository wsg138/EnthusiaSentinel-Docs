# Operator escalation

Most repository work should be solvable without private control-plane access. Escalate to the Sentinel operator only for owner-controlled changes or service faults.

## Escalate for

- initial onboarding or re-enrollment;
- installation/repository mapping changes in Sentinel trusted policy;
- manager additions/removals;
- profile/automatic-transition/fork-policy increases;
- dependency registry changes or expired/inaccessible trusted locks;
- a reproducible Sentinel service, reporting, installation-token, queue, or isolation defect;
- a required behavior that the public manifest/profile model does not safely express.

## Include

Provide repository full name and immutable repository ID if known, PR number, exact SHA, command/profile, GitHub check/comment, bounded Sentinel result code/summary, and the relevant Actions run for the target artifact.

## Never include

Do not send GitHub App private keys, installation tokens/JWTs, SSH keys, internal database credentials, production Minecraft data, private control-plane configuration dumps, or unrelated private repository data.

## Operator-only implementation details

The private Sentinel control repository remains authoritative for runtime implementation, deployment, protected policy, dependency locks, host recovery, and security acceptance. This public repository intentionally documents user contracts rather than sensitive topology.
