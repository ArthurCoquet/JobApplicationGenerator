from pydantic import BaseModel


class PersonalInfo(BaseModel):
    first_name: str
    last_name: str
    title: str
    picture: str
    description: str


class ContactInfo(BaseModel):
    phone: str
    LinkedIn: str
    GitHub: str
    location: str
    driving_license: str


class ExpertiseInfo(BaseModel):
    coding_langauges: list[str]
    tools: list[str]
    softwares: list[str]
    languages: list[str]
    Hobbies: list[str]


class Experience(BaseModel):
    id: str
    title: str
    company: str | None = None
    location: str | None = None
    timeframe: str
    bulletpoints: list[str]


class Education(BaseModel):
    title: str
    bulletpoints: list[str]


class Section(BaseModel):
    personal_info: PersonalInfo
    contact_info: ContactInfo
    expertise_info: ExpertiseInfo
    pro_experiences: list[Experience]
    education: list[Education]


class Resume(BaseModel):
    layout: int
    sections: Section