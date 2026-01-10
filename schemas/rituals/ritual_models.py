from pydantic import BaseModel
from typing import Dict, Any


class RitualRequest(BaseModel):
    user_id: int


class RitualResponse(BaseModel):
    status: str
    date: str
    data: Dict[str, Any]
