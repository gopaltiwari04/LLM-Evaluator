from uuid import UUID

from pydantic import BaseModel, Field


class APIKeyCreate(BaseModel):
    project_id: UUID
    name: str = Field(min_length=1, max_length=255)


class APIKeyResponse(BaseModel):
    id: UUID
    project_id: UUID
    name: str
    api_key: str