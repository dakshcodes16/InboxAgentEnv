from pydantic import BaseModel
from typing import Any, Dict

class Action(BaseModel):
    action_type: str
    params: Dict[str, Any]

class Observation(BaseModel):
    state: Dict[str, Any]
    output: Any = None
    error: str | None = None

class Reward(BaseModel):
    score: float
    is_done: bool
    message: str | None = None
