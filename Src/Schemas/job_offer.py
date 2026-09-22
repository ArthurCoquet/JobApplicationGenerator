from pydantic import BaseModel, ConfigDict
from typing import Any
from Schemas.job_analysis import JobAnalysisResponse
from Schemas.retrieval import Retrieval
from Schemas.rerank_format import MinimalistRerank
from Schemas.write_resume import Resume
from Schemas.write_plan import LetterPlan
from Schemas.write_cover_letter import CoverLetter

class JobOffer(BaseModel):
    model_config = ConfigDict(extra="allow")

    title: str
    url: str
    content: str

    offer_analysis: JobAnalysisResponse | None = None

    retrieval: Retrieval | None = None
    rerank: MinimalistRerank | None = None
    top_experiences_names: list[str] | None = None

    personal_facts: dict[str, Any] | None = None

    resume: Resume | None = None
    plan: LetterPlan | None = None
    cover_letter: CoverLetter | None = None
    