from config.settings import Settings
from Helpers.OfferRepository import OfferRepository
from Infrastructures.llm_inference import LlmInference
from Schemas.write_resume import Resume

class ResumeWriter:

    def __init__(
            self,
            llm: LlmInference,
            settings: Settings,
            offer_repo: OfferRepository
        ) -> None:

        self.llm = llm
        self.offer_repo = offer_repo
        self.settings = settings

    def write_resume(
        self,
        offer_path: str
    ) -> None:
        
        data = self.offer_repo.load(path=offer_path)

        llm_data = {
            key: value
            for key, value in data.items()
            if key != "rerank"
        }

        # Ecriture du plan de rédaction par le llm

        resume = self.llm.chat_completion_with_format(
            content=str(llm_data), 
            response_format=Resume, 
            system_prompt_path=self.settings.resume_writing_system_prompt_path
        )

        data["resume"] = resume

        self.offer_repo.save(path=offer_path, data=data)
        
