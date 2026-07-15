from typing import Optional

from pydantic import BaseModel, Field, model_validator


class IngestRequest(BaseModel):
    url: Optional[str] = None
    text: Optional[str] = None

    @model_validator(mode="after")
    def exactly_one_source(self):
        if bool(self.url) == bool(self.text):
            raise ValueError("exactly one of 'url' or 'text' is required")
        return self


class DocumentOut(BaseModel):
    id: int
    url: Optional[str]
    source_type: str
    created_at: str
    updated_at: str


class DocumentDetail(DocumentOut):
    content: str


class AskRequest(BaseModel):
    question: str = Field(min_length=1)
