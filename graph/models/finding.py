from pydantic import BaseModel, Field


class Finding(BaseModel):
    severity: int = Field(
        ge=1,
        le=10,
        description="Severity of the issue from 1 to 10, where 1 is minimal and 10 is extremely severe."
    )

    category: str = Field(
        description="Category of the issue: bug, security, performance, or code_quality."
    )

    description: str = Field(
        description="Clear and concise description of the issue."
    )

    suggestion: str = Field(
        description="Practical and actionable suggestion to fix the issue."
    )
    file:str = Field(
        description="File path of the issue."
    )
    line:int = Field(
        description="Line number of the issue."
    )