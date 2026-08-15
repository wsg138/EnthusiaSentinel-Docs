# Profiles

A profile can run only when Sentinel supports it, the repository manifest declares the required bounded inputs, and trusted repository policy allows it. Repositories should request the smallest useful set.

| Profile | Purpose | Typical success |
|---|---|---|
| `startup` | One disposable Paper startup with the target plugin | `PAPER_SMOKE_OK` |
| `restart` | Two sequential Paper cycles with restart persistence | `PAPER_RESTART_OK` |
| `restart-config` | Restart with exact-artifact config fixtures/assertions | `PAPER_RESTART_CONFIG_OK` |
| `reload-config` | One bounded reload command with reviewed config edits/assertions | `PAPER_RELOAD_CONFIG_OK` |
| `database` | Approved SQLite fixture/schema/canary regression checks | `PAPER_DATABASE_OK` |
| `dependencies` | Start with exact trusted dependency artifacts | `PAPER_DEPENDENCIES_OK` |
| `java-client` | One fixed credential-free synthetic Java client | `JAVA_CLIENT_OK` |
| `java-interaction` | Two fixed credential-free Java interaction clients | `JAVA_INTERACTION_OK`-family terminal result |
| `bedrock-client` | Controlled local Geyser/Floodgate-compatible boundary | `BEDROCK_CLIENT_OK` |
| `full` | Sequential bounded composition of applicable declared profiles | `FULL_PROFILE_OK` |
| `post-merge` | Strongest safe merge-oriented composition on actual merge SHA | profile aggregate success |

## Manual-only vs automatic

`dependencies` is manual-only. A repository can also be configured entirely manual-only, meaning no PR lifecycle transition creates work. Automatic repositories can have separately reviewed profiles for opened, ready, reviewable-head, and merged transitions.

## Profile authorization is a ceiling

A manifest does not grant a profile. A GitHub App installation does not grant a profile. A repository manager cannot add a profile through commands. Expanding the allowlist is a Sentinel-owner-reviewed privilege increase.
