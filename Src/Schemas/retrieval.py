from pydantic import BaseModel
from Schemas.job_analysis import Need


class RetrievedChunk(BaseModel):
    section: str
    content: str
    retrieved_for: list[str]


class RetrievedExperience(BaseModel):
    experience: str
    chunks: list[RetrievedChunk]


class Retrieval(BaseModel):
    needs: list[Need]
    experiences: list[RetrievedExperience]