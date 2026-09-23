from config.settings import Settings
from Infrastructures.llm_inference import LlmInference
from Schemas.write_resume import Resume
from Schemas.job_offer import JobOffer
import json 

class ResumeWriter:

    def __init__(
            self,
            llm: LlmInference,
            settings: Settings,
        ) -> None:

        self.llm = llm
        self.settings = settings

    def write_resume(
        self,
        job_offer: JobOffer
    ) -> None:
        
        llm_data = job_offer.model_dump(
            exclude={"rerank", "resume"}
        )

        # Ecriture du plan de rédaction par le llm

        job_offer.resume = self.llm.generate_structured_response(
            content=json.dumps(
                llm_data,
                ensure_ascii=False
            ), 
            response_format=Resume, 
            system_prompt_path=self.settings.resume_writing_system_prompt_path
        )        
