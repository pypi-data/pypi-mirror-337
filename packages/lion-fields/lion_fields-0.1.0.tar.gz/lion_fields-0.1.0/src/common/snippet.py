from enum import Enum

from pydantic import Field

from .models import HashableModel


class ContentType(str, Enum):
    """Distinct snippet types used to identify the content category."""

    TEXT = "text"
    CODE = "code"


class BaseSnippet(HashableModel):
    """
    Base snippet with a content type and optional note.
    Subclasses define their own 'content' fields.
    """

    type: ContentType
    note: str | None = Field(
        default=None,
        description="Extra context or metadata about this snippet",
    )


class TextSnippet(BaseSnippet):
    """Plain text snippet (paragraphs, bullet points, etc.)."""

    type: ContentType = Field(
        default=ContentType.TEXT,
        description="Must be 'text'. Identifies a text snippet.",
        frozen=True,
    )
    content: str = Field(
        default_factory=str,
        description="The actual text. Use paragraphs, lists, etc. as needed.",
    )


class CodeSnippet(BaseSnippet):
    """Code/command snippet with language specified."""

    type: ContentType = Field(
        default=ContentType.CODE,
        description="Must be 'code'. Identifies a code snippet.",
        frozen=True,
    )
    content: str = Field(
        default_factory=str,
        description="The raw code or commands, preserving indentation.",
    )
    language: str = Field(
        default_factory=str,
        description="Language name (e.g., 'python', 'bash', 'rust', 'pseudocode').",
    )
