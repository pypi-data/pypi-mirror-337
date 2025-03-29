from typing import Any

from pydantic import Field, JsonValue

from .common import HashableModel

__all__ = (
    "Instruct",
    "InstructResponse",
)


class Instruct(HashableModel):
    """Model for defining instruction parameters and execution requirements."""

    instruction: JsonValue | None = Field(
        None,
        title="Primary Instruction",
        description=(
            "A clear, actionable task definition. Specify:\n"
            "1) The primary goal or objective\n"
            "2) Key success criteria or constraints\n"
            "\n"
            "Guidelines:\n"
            "- Start with a direct action verb (e.g., 'Analyze', 'Generate', 'Create')\n"
            "- Include scope, boundaries, or constraints\n"
            "- Provide success criteria if relevant\n"
            "- For complex tasks, break them into logical steps"
        ),
    )
    guidance: JsonValue | None = Field(
        None,
        title="Guidance",
        description=(
            "Strategic direction and constraints for executing the task. "
            "Include:\n"
            "1) Preferred methods or frameworks\n"
            "2) Quality benchmarks (e.g., speed, clarity)\n"
            "3) Resource or environmental constraints\n"
            "4) Relevant compliance or standards\n"
            "Use None if no special guidance."
        ),
    )
    context: JsonValue | None = Field(
        None,
        description=(
            "Background information and current-state data needed for the task. "
            "Should be:\n"
            "1) Directly relevant\n"
            "2) Sufficient to perform the task\n"
            "3) Free of extraneous detail\n"
            "Include environment, prior outcomes, system states, or dependencies. "
            "Use None if no additional context is needed."
        ),
    )


class InstructResponse(HashableModel):
    instruct: Instruct
    response: Any | None = None
