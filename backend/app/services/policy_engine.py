"""Task run-safe policy evaluation helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.models.board_policies import BoardPolicy
from app.models.tasks import Task
from app.schemas.board_policies import TaskPolicyViolation, TaskRunSafeValidation

POLICY_NO_BASELINE_NO_DEV = "no_baseline_no_dev"
POLICY_NO_ACCEPTANCE_NO_DEV = "no_acceptance_no_dev"
POLICY_REQUIRE_EVIDENCE_BEFORE_DONE = "require_evidence_before_done"
DEFAULT_POLICY_KEYS = {
    POLICY_NO_BASELINE_NO_DEV,
    POLICY_NO_ACCEPTANCE_NO_DEV,
    POLICY_REQUIRE_EVIDENCE_BEFORE_DONE,
}


@dataclass(slots=True)
class PolicyEvaluationContext:
    """Normalized runtime inputs for policy checks."""

    task: Task
    policies: dict[str, BoardPolicy] = field(default_factory=dict)
    evidence_kinds: set[str] = field(default_factory=set)
    open_blocker_count: int = 0


def _is_policy_enabled(ctx: PolicyEvaluationContext, key: str) -> bool:
    policy = ctx.policies.get(key)
    if policy is None:
        return False
    return bool(policy.enabled)


def _required_evidence_kinds(ctx: PolicyEvaluationContext) -> set[str]:
    policy = ctx.policies.get(POLICY_REQUIRE_EVIDENCE_BEFORE_DONE)
    if policy is None or not policy.enabled:
        return set()
    raw = policy.config_json.get("required_evidence_kinds") if policy.config_json else None
    if not isinstance(raw, list):
        return set()
    return {str(item).strip() for item in raw if str(item).strip()}


def _has_baseline(task: Task) -> bool:
    value = task.baseline_ref
    return isinstance(value, dict) and bool(value.get("value"))


def _has_acceptance(task: Task) -> bool:
    value = task.acceptance_checklist
    return isinstance(value, list) and any(str(item).strip() for item in value)


def evaluate_task_readiness(ctx: PolicyEvaluationContext) -> TaskRunSafeValidation:
    """Evaluate whether a task is safe to start."""

    violations: list[TaskPolicyViolation] = []
    actions: list[str] = []
    status = "ready"

    if _is_policy_enabled(ctx, POLICY_NO_BASELINE_NO_DEV) and not _has_baseline(ctx.task):
        violations.append(
            TaskPolicyViolation(
                policy=POLICY_NO_BASELINE_NO_DEV,
                message="Task is missing baseline_ref.",
            ),
        )
        actions.append("Add a baseline reference before moving the task into progress.")
        status = "blocked_missing_baseline"

    if _is_policy_enabled(ctx, POLICY_NO_ACCEPTANCE_NO_DEV) and not _has_acceptance(ctx.task):
        violations.append(
            TaskPolicyViolation(
                policy=POLICY_NO_ACCEPTANCE_NO_DEV,
                message="Task is missing acceptance_checklist.",
            ),
        )
        actions.append("Add 3-7 testable acceptance items before starting execution.")
        if status == "ready":
            status = "blocked_missing_acceptance"

    return TaskRunSafeValidation(
        ok=not violations,
        status=status,
        violations=violations,
        recommended_actions=actions,
    )


def evaluate_task_completion(ctx: PolicyEvaluationContext) -> TaskRunSafeValidation:
    """Evaluate whether a task is safe to move to review/done."""

    violations: list[TaskPolicyViolation] = []
    actions: list[str] = []
    status = "ready"

    required_kinds = _required_evidence_kinds(ctx)
    missing_required = sorted(required_kinds - ctx.evidence_kinds)
    if missing_required:
        violations.append(
            TaskPolicyViolation(
                policy=POLICY_REQUIRE_EVIDENCE_BEFORE_DONE,
                message=(
                    "Task is missing required evidence kinds: " + ", ".join(missing_required)
                ),
            ),
        )
        actions.append("Attach the required evidence before completing the task.")
        status = "blocked_missing_evidence"

    if ctx.open_blocker_count > 0:
        violations.append(
            TaskPolicyViolation(
                policy="open_blockers_prevent_completion",
                message="Task still has unresolved blockers.",
            ),
        )
        actions.append("Resolve or mitigate open blockers before completion.")
        if status == "ready":
            status = "blocked_open_blockers"

    return TaskRunSafeValidation(
        ok=not violations,
        status=status,
        violations=violations,
        recommended_actions=actions,
    )


def update_task_run_safe_fields(task: Task, validation: TaskRunSafeValidation) -> None:
    """Copy validation result back onto the task model."""

    task.run_safe_status = validation.status


def default_policy_config(policy_key: str) -> dict[str, Any]:
    """Return default config for known policies."""

    if policy_key == POLICY_REQUIRE_EVIDENCE_BEFORE_DONE:
        return {"required_evidence_kinds": ["commit", "repro_steps"], "warning_only": False}
    return {}
