import uuid

from pydantic import BaseModel, Field


class Activity(BaseModel, from_attributes=True):
    guid: uuid.UUID

    name: str

    description: str
    prompt: str

    sources: str
    authors: str

    topics: set[uuid.UUID] = Field(default_factory=set)

    def __hash__(self) -> int:
        return hash(self.guid)
