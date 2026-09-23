from Infrastructures.llm_inference import LlmInference
import logging
from Schemas.rerank_format import MinimalistRerank
from Schemas.job_offer import JobOffer
from config.settings import Settings
import json

logger = logging.getLogger(__name__)

class ExperienceReranker:

    def __init__(
            self,
            llm: LlmInference,
            settings: Settings,
            system_prompt_path: str | None = None,
        ) -> None:

        self.llm = llm
        
        self.system_prompt_path = system_prompt_path or settings.reranking_system_prompt_path

    def rerank_experiences(self, job_offer: JobOffer) -> None:

        if job_offer.retrieval is None:
            raise ValueError("retrieval has not been computed yet")

        retrieval_content = json.dumps(
            job_offer.retrieval.model_dump(),
            ensure_ascii=False
        )

        job_offer.rerank = self.llm.generate_structured_response(
            content=retrieval_content, 
            response_format=MinimalistRerank, 
            system_prompt_path=self.system_prompt_path
        )

        logger.info("Done reranking experiences")