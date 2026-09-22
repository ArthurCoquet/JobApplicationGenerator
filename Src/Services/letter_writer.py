from Infrastructures.llm_inference import LlmInference
from Schemas.write_plan import LetterPlan
from Helpers.OfferRepository import OfferRepository
from config.settings import Settings
from Schemas.write_cover_letter import CoverLetter
import json

class LetterWriter:

    def __init__(
            self,
            llm: LlmInference,
            offer_repo: OfferRepository,
            settings: Settings
        ) -> None:

        self.llm = llm
        self.offer_repo = offer_repo
        self.settings = settings


    def write_cover_letter(
            self,
            offer_path: str
        ):

        data = self.offer_repo.load(offer_path)

        plan_context = {
            key: value
            for key, value in data.items()
            if key not in {"rerank", "resume"}
        }

        content=json.dumps(
            plan_context,
            ensure_ascii=False,
            indent=2
        )

        # Ecriture du plan de rédaction par le llm
        plan = self.llm.chat_completion_with_format(
            content=str(content), 
            response_format=LetterPlan, 
            system_prompt_path=self.settings.plan_writing_system_prompt_path
        )

        data["plan"] = plan

        self.offer_repo.save(offer_path, data)

        letter_context = {
            **plan_context,
            "plan": plan
        }

        content=json.dumps(letter_context, ensure_ascii=False, indent=2)

        ## Rédaction de la lettre de motivation par le llm
        letter = self.llm.chat_completion_with_format(
            content=content, 
            response_format=CoverLetter,
            system_prompt_path=self.settings.cover_letter_writing_system_prompt_path
        )

        data["letter"] = letter

        self.offer_repo.save(offer_path, data)
