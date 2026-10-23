from pydantic import BaseModel, Field


class Experience(BaseModel):
    id: str
    title: str
    company: str | None = None
    location: str | None = None
    timeframe: str
    bulletpoints: list[str] = Field(max_length=4)


class Resume(BaseModel):
    job_title: str
    profile_summary: str
    experiences: list[Experience] 