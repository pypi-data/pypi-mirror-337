from .common import CodeSnippet, Field, HashableModel, Source, TextSnippet

__all__ = (
    "ResearchFinding",
    "PotentialRisk",
    "ResearchSummary",
)


class ResearchFinding(HashableModel):
    """
    A single piece of information or insight from the research phase.
    """

    summary: str = Field(
        ...,
        description="Concise text describing the discovered fact, concept, or best practice.",
    )
    snippets: list[TextSnippet | CodeSnippet] = Field(
        default_factory=list,
        description="Ordered list of content snippets (text or code) that illustrate or support the finding.",
    )
    relevance: str | None = Field(
        default=None,
        description="Why this finding matters to the project. E.g., 'Helps solve concurrency issue.'",
    )
    sources: list[Source] = Field(
        default_factory=list,
        description="One or more references (e.g., docs, blog posts) supporting this finding.",
    )


class PotentialRisk(HashableModel):
    """
    Identifies a risk or challenge discovered during research.
    """

    description: str = Field(
        ...,
        description="Short text describing the risk. E.g., 'Scalability concerns with chosen DB'.",
    )
    impact: str | None = Field(
        default=None,
        description="Possible consequences if not mitigated. E.g., 'System slowdown, possible downtime.'",
    )
    mitigation_ideas: str | None = Field(
        default=None, description="Preliminary ways to reduce or handle this risk."
    )
    sources: list[Source] = Field(
        default_factory=list,
        description="References confirming or highlighting this risk.",
    )


class ResearchSummary(HashableModel):
    """
    Captures the final outcome of the deep research process.
    """

    scope: str | None = Field(
        default=None,
        description="Brief statement of what was investigated. E.g., 'Surveyed python-based ORMs.'",
    )
    main_takeaways: str = Field(
        ...,
        description="High-level summary of the most critical insights for the project.",
    )
    findings: list[ResearchFinding] = Field(
        default_factory=list, description="List of key facts or knowledge gained."
    )
    risks: list[PotentialRisk] = Field(
        default_factory=list,
        description="Identified obstacles or concerns for the project.",
    )
