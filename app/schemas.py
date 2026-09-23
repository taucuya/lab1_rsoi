from typing import Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class PersonRequest(BaseModel):
    name: str = Field(min_length=1)
    age: Optional[int] = None
    address: Optional[str] = None
    work: Optional[str] = None


class PersonResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    age: Optional[int] = None
    address: Optional[str] = None
    work: Optional[str] = None


class ErrorResponse(BaseModel):
    message: str


class ValidationErrorResponse(BaseModel):
    message: str = "Invalid data"
    errors: Dict[str, str] = Field(default_factory=dict)
