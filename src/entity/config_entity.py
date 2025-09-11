
from pydantic import BaseModel
from typing import List

class PredictionOutput(BaseModel):
    risk_level: str
    events: List[str]
    rationale: str
