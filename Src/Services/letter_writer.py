from Infrastructures.llm_inference import LlmInference
from Schemas.job_offer import JobOffer
from Schemas.write_plan import LetterPlan
from config.settings import Settings
from Schemas.write_cover_letter import CoverLetter
import json

class LetterWriter:

    def __init__(
            self,
            llm: LlmInference,
            settings: Settings
        ) -> None:

        self.llm = llm
        self.settings = settings


    def write_cover_letter_plan(
            self,
            job_offer: JobOffer
    ) -> None:

        plan_context = job_offer.model_dump(
            exclude={"rerank","resume"}
        )

        content=json.dumps(
            plan_context,
            ensure_ascii=False,
            indent=2
        )

        # Ecriture du plan de rédaction par le llm
        job_offer.plan = self.llm.chat_completion_with_format(
            content=content, 
            response_format=LetterPlan, 
            system_prompt_path=self.settings.plan_writing_system_prompt_path
        )

    def write_cover_letter(
            self,
            job_offer: JobOffer
    ) -> None:

        letter_context = job_offer.model_dump(
            exclude={"rerank", "resume"}
        )

        content=json.dumps(letter_context, ensure_ascii=False, indent=2)

        ## Rédaction de la lettre de motivation par le llm
        job_offer.cover_letter = self.llm.chat_completion_with_format(
            content=content, 
            response_format=CoverLetter,
            system_prompt_path=self.settings.cover_letter_writing_system_prompt_path
        )
        