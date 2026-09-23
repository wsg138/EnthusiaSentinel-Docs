# Testing EnthusiaSentinel-Docs

This repository contains public/onboarding Sentinel documentation and example build/manifest files. Its tests are **documentation/example integrity checks**. They do not execute Sentinel Sim itself and they do not replace the private runtime, plugin, Pi, Bloom, or release validation described by Sentinel's canonical engineering repositories.

## Automated checks

`test/test_repository_integrity.py` validates the examples and repository-local documentation contracts.

### Manifest examples

Every `examples/manifests/*.yml` file is parsed with `yaml.safe_load` and checked for:

- schema version `1`;
- the documented top-level keys (`plugin`, `artifact`, `profiles`, `configs`, `databases`, `dependencies`, and `actions`);
- list-shaped collection fields;
- a safe lower-case plugin id;
- nonblank plugin/artifact names;
- a qualified main class;
- repository-relative `.jar` paths that cannot escape with `..`;
- at least one nonblank, unique profile;
- nonblank and unique dependency ids with explicit dependency kinds.

The tests intentionally validate the documented example contract without inventing private registry values or production dependency provenance.

### Build examples

The Maven example is parsed as XML and must retain:

- Maven model `4.0.0`;
- Java release `21`;
- final artifact name `SentinelExample`.

The Gradle Kotlin DSL example must retain:

- Java toolchain 21;
- `SentinelExample.jar` as the documented artifact;
- the documented Gradle build command and `build/libs/SentinelExample.jar` path.

These are documentation contract checks. They do not download Gradle/Maven dependencies or compile a sample plugin.

### Markdown links

All Markdown files are scanned for repository-local links. Relative links must:

- remain inside this repository;
- point to a file/directory that exists.

HTTP(S), mail, data, root-relative site routes, and same-page anchor-only links are intentionally not fetched by CI.

## Running locally

Requires Python 3 and PyYAML 6.0.2.

```bash
python -m pip install PyYAML==6.0.2
python -m unittest discover -s test -p 'test_*.py' -v
```

No Sentinel credentials, GitHub App key, plugin artifacts, database, Pi, or Bloom access is required.

## CI

`.github/workflows/tests.yml` runs the same suite on pull requests and pushes to `main` with Python 3.13.

A green result means the documentation/examples on that **exact Git commit** satisfy the repository's integrity rules. If a workflow never receives a runner and has no executed steps, record that as infrastructure-only; do not call the documentation validated.

## How to interpret failures

### YAML parse/schema failure

Check the example itself first. If Sentinel's public manifest contract intentionally changed, update the example, test contract, and the corresponding documentation together. Do not loosen the test simply to preserve an obsolete example.

### Unsafe artifact path

Public examples must not teach absolute paths or repository escapes for their build artifact. Correct the example unless the canonical Sentinel contract explicitly changed and was reviewed elsewhere first.

### Duplicate/blank profile or dependency id

Treat this as an invalid onboarding example. Example manifests should be deterministic and unambiguous.

### Maven/Gradle example failure

Reconcile the example with the current supported Java/build contract. If Java/tooling support changed intentionally, update both examples and all public instructions that reference them.

### Broken local Markdown link

Usually a document was renamed/moved without its references being updated. Fix the reference or restore the intended document. Do not replace a valid relative documentation link with an external URL merely to silence CI.

## What this repository does not prove

These tests do **not** prove:

- `EnthusiaSentinel-Sim` compiles or passes its Java tests;
- a plugin manifest is accepted by the current Sentinel parser/runtime;
- a sample plugin actually builds under Maven/Gradle;
- GitHub App artifact/repository/SHA identity verification works;
- MockBukkit or real-Paper lifecycles pass;
- private/manual-only dependency profiles are authorized;
- Pi/Bloom/staging/production compatibility is healthy;
- release artifacts, checksums, or credentials are valid.

Those checks belong in Sentinel Sim, the plugin repository, or the applicable controlled runtime/staging process. Public documentation tests should never require production credentials or private plugin data.

## Review/maintenance rule

When changing a public Sentinel example or onboarding instruction:

1. confirm the change matches the current canonical Sentinel contract;
2. update the relevant example and documentation together;
3. add/adjust a deterministic integrity assertion if a new public contract is introduced;
4. run this repository's test suite;
5. record exact-head CI evidence;
6. separately validate Sentinel Sim/runtime behavior when the change describes a runtime capability rather than documentation only.
