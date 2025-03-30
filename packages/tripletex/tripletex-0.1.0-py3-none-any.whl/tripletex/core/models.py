from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class TripletexResponse(BaseModel, Generic[T]):
    full_result_size: Optional[int] = Field(None, alias="fullResultSize")
    from_index: Optional[int] = Field(None, alias="from")
    count: int
    version_digest: Optional[str] = Field(None, alias="versionDigest")
    values: List[T]

    class Config:
        populate_by_name = True


class IdUrl(BaseModel):
    id: int
    url: str


class Change(BaseModel):
    employee_id: Optional[int] = Field(None, alias="employeeId")
    timestamp: Optional[str] = None
    change_type: Optional[str] = Field(None, alias="changeType")
