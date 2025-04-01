from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Meta(BaseModel):
    authorization: Optional[dict] = {}
    timestamp: datetime
    correlation_id: str
    ip: str
