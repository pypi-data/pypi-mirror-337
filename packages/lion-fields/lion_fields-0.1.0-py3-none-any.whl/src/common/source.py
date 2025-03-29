from pydantic import Field, HttpUrl

from .models import HashableModel


class Source(HashableModel):
    """External reference (web link, file path, etc.)."""

    url: HttpUrl | str = Field(
        default_factory=str,
        description="A valid URL or resource identifier. E.g., 'https://...' or 'path/to/file'.",
    )
    title: str = Field(
        default_factory=str,
        description="Short descriptive name for this source.",
    )
    description: str | None = Field(
        default=None,
        description="Optional summary of how/why this source is relevant.",
    )
