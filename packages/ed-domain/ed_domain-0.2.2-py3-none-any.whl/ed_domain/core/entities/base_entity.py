from datetime import datetime
from typing import TypedDict
from uuid import UUID


class BaseEntity(TypedDict):
    id: UUID
    created_datetime: datetime
    updated_datetime: datetime
    deleted: bool
