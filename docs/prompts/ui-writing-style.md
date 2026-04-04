# UI writing style

## Purpose

This document defines the writing style for Mission Control UI text so that labels, statuses, action names, and feedback messages remain consistent across the product.

## Audience

- frontend contributors
- product and UX collaborators
- reviewers checking wording consistency

## Principles

### Be direct

UI copy should say what is happening or what will happen.
Prefer concrete verbs and short phrases over abstract wording.

### Be operationally clear

Mission Control is an internal operations product.
The UI should optimize for clarity, not brand voice.

### Be specific about outcomes

When an action succeeds, fails, or is unavailable, say so explicitly.
Avoid wording that leaves the user guessing whether the system accepted the request.

### Avoid false certainty

If the system is waiting, uncertain, or stale, do not write copy that implies a final result is already known.

## Action labels

Prefer action labels that begin with clear verbs.

Preferred examples:

- Refresh state
- View details
- View logs
- Retry task
- Cancel run

Avoid vague labels such as:

- Process
- Execute
- Handle
- Submit

## Status labels

Status labels should be short and visually scannable.
They should distinguish between different end states rather than collapsing them into generic wording.

Preferred examples:

- Active
- Idle
- Running
- Failed
- Cancelled
- Succeeded
- Waiting

## Error messages

Good error messages should help the user decide what to do next.

Preferred pattern:

- what failed
- why it failed, if known
- what to do next, if useful

Example:

- `Retry failed: this run is no longer eligible for retry.`
- `Refresh failed: Mission Control could not reach the runtime. Try again in a moment.`

Avoid generic messages when a more specific cause is available.

## Empty states

Empty states should explain whether:

- there is simply no data yet
- filters excluded all results
- the system could not load the data

An empty state should not look the same as an error state.

## Success feedback

Success feedback should confirm acceptance or completion clearly.
If the system is asynchronous, the message should say whether the action has completed or is only requested.

Examples:

- `Retry requested.`
- `Cancellation requested.`
- `State refreshed.`

## Tone

Mission Control copy should be:

- calm
- precise
- low-drama
- low-ambiguity

It should not be:

- playful in operational contexts
- marketing-oriented
- overly verbose
