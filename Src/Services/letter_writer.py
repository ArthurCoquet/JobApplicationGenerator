from Infrastructures.llm_inference import LlmInference
from Schemas.write_plan import LetterPlan
from Helpers.OfferRepository import OfferRepository
from config.settings import Settings
from Schemas.write_cover_letter import formatLibre

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

        llm_data = {
            key: value
            for key, value in data.items()
            if key not in {"rerank", "resume"}
        }

        # Ecriture du plan de rédaction par le llm
        plan = self.llm.chat_completion_with_format(
            content=str(llm_data), 
            response_format=LetterPlan, 
            system_prompt_path=self.settings.plan_writing_system_prompt_path
        )

        data["plan"] = plan

        self.offer_repo.save(offer_path, data)

        ## Rédaction de la lettre de motivation par le llm
        letter = self.llm.chat_completion_with_format(
            content=str(llm_data), 
            response_format=formatLibre,
            system_prompt_path=self.settings.cover_letter_writing_system_prompt_path
        )

        data["letter"] = letter

        self.offer_repo.save(offer_path, data)
