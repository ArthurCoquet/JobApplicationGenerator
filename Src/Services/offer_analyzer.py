from Infrastructures.llm_inference import LlmInference
from Helpers.OfferRepository import OfferRepository
from config.settings import Settings
from Schemas.job_analysis import JobAnalysisResponse
from Schemas.job_offer import JobOffer    

class OfferAnalyzer:

    def __init__(
            self,
            llm: LlmInference,
            offer_repo: OfferRepository,
            settings: Settings
            ) -> None:

        self.llm = llm
        self.offer_repo = offer_repo
        self.settings = settings
        
    def analyze(
            self,
            job_offer: JobOffer
        ):
        
        job_offer.offer_analysis = self.llm.chat_completion_with_format(
            content=job_offer.content, 
            response_format=JobAnalysisResponse, 
            system_prompt_path=self.settings.offer_analysis_system_prompt_path)
