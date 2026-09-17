from pydantic import BaseModel, Field
from graph.models.finding import Finding

class Review(BaseModel):
    """Structured review of the provided code."""

    text: str = Field(
        description="A concise overall review of the code."
    )

    findings: list[Finding] = Field(
        description="Genuine and actionable issues identified in the code."
    )
