# Release checklist

## Purpose

This document defines the minimum release-readiness checks for Mission Control so that product, documentation, and runtime-facing behavior stay aligned.

## Audience

- maintainers preparing a release
- reviewers performing release readiness checks
- contributors verifying whether a change is safe to ship

## What this document does not cover

This document does not replace:

- rollback procedures
- incident response playbooks
- low-level CI implementation details

## Minimum release checklist

### 1. Scope clarity

Confirm that the release scope is understandable.

- [ ] The intended user-visible changes are known
- [ ] High-risk changes are identified
- [ ] Documentation-impacting changes are identified

### 2. Documentation alignment

Confirm that docs match behavior.

- [ ] Product-facing changes are reflected in the relevant docs
- [ ] Action or state changes are reflected in reference or contract docs
- [ ] New pages or workflows are documented at the right layer

### 3. Core product sanity

Confirm the minimum user path still works.

- [ ] App starts in the expected release environment
- [ ] Main shell or landing route loads
- [ ] At least one primary list view works
- [ ] At least one primary detail view works

### 4. Action safety

Confirm write actions still behave safely.

- [ ] High-value actions have understandable feedback
- [ ] Unavailable actions are correctly gated
- [ ] Failure paths still explain what happened

### 5. Runtime integration sanity

Confirm runtime-facing behavior is still coherent.

- [ ] Read paths still return expected object state
- [ ] Action paths still map cleanly to downstream behavior
- [ ] State refresh behavior is still understandable

### 6. Regression confidence

Confirm test and verification evidence is enough for the scope.

- [ ] Relevant automated checks passed
- [ ] Manual spot checks were performed where needed
- [ ] Known gaps are documented if anything was intentionally deferred

## Release decision

Before release, the reviewer should be able to answer:

- What changed?
- What is the user impact?
- What is the runtime impact?
- What would likely fail first if something is wrong?
