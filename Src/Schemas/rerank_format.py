from pydantic import BaseModel
from typing import List, Literal

class ExperienceEvaluation(BaseModel):
    experience: str
    score: int
    rank: int
    decision: Literal["reject", "possible", "strong_match"]
    reason: str


class Reranker(BaseModel):
    experiences: List[ExperienceEvaluation]