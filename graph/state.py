from typing import TypedDict

from graph.chains.code_reviewer import Finding


class GraphState(TypedDict):
    """State shared across the graph."""
    code: str
    needs_context: bool
    context: str
    findings: list[Finding]
    file_path: str | None
    context_requests: int
    human_decision: str | None
    github_review_url: str | None
