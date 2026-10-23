from pydantic import BaseModel
from typing import Literal


class Need(BaseModel):
    name: str
    priority: Literal["core", "secondary", "optional"]
    description: str
    source_excerpt: str


class Requirement(BaseModel):
    name: str
    importance: Literal["mandatory", "preferred"]
    source_excerpt: str


class JobAnalysisResponse(BaseModel):
    needs: list[Need]
    requirements: list[Requirement]