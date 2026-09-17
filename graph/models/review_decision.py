from pydantic import BaseModel


class ReviewDecision(BaseModel):
    needs_context: bool
    file_path: str | None
    reason: str | None