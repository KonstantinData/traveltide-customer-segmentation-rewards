"""EDA workflow definition loader and helpers."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class EDAWorkflowStep:
    """Single workflow step definition."""

    id: str
    title: str
    purpose: str
    note: str


@dataclass(frozen=True)
class EDAWorkflow:
    """EDA workflow definition."""

    name: str
    description: str
    steps: tuple[EDAWorkflowStep, ...]


def load_workflow(path: str | Path) -> EDAWorkflow:
    """Load the EDA workflow definition from eda.yml."""

    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "eda_workflow" not in data:
        raise ValueError("eda.yml must contain an 'eda_workflow' mapping")

    wf = data["eda_workflow"]
    steps = tuple(EDAWorkflowStep(**step) for step in wf.get("steps", []))
    if not steps:
        raise ValueError("eda.yml must define at least one workflow step")

    return EDAWorkflow(
        name=wf.get("name", "EDA Workflow"),
        description=wf.get("description", ""),
        steps=steps,
    )


def workflow_to_dict(workflow: EDAWorkflow) -> dict[str, Any]:
    """Serialize workflow to a dict suitable for metadata/report output."""

    return {
        "name": workflow.name,
        "description": workflow.description,
        "steps": [asdict(step) for step in workflow.steps],
    }


def annotate_steps(
    workflow: EDAWorkflow, outputs: dict[str, list[str] | dict[str, Any]]
) -> list[dict[str, Any]]:
    """Attach status + outputs to workflow steps for reporting."""

    annotated = []
    for step in workflow.steps:
        step_outputs = outputs.get(step.id, [])
        annotated.append(
            {
                "id": step.id,
                "title": step.title,
                "purpose": step.purpose,
                "note": step.note,
                "status": "complete",
                "outputs": step_outputs,
            }
        )
    return annotated
