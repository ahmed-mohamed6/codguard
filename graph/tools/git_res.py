from pydantic import BaseModel


class ChangedFile(BaseModel):
    filename: str
    status: str
    additions: int
    deletions: int
    changes: int
    patch: str | None = None