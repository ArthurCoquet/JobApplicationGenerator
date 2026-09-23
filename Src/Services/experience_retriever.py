from Services.write_queries import write_queries
from Infrastructures.vector_search import VectorSearch
from config.settings import Settings
from Schemas.job_offer import JobOffer
from Schemas.retrieval import Retrieval

class ExperienceRetriever:

    def __init__(
            self,
            settings: Settings,
            vector_search: VectorSearch
        ) -> None:

        self.settings = settings
        self.vector_search = vector_search

    async def retrieve_experience(
            self,
            job_offer: JobOffer
    ):

        queries = write_queries(job_offer)

        grouped_batch, _ready_for_rerank = await self.vector_search.retrieval_batch(queries)

        if job_offer.offer_analysis is None:
            raise ValueError("offer_analysis has not been computed yet")
        
        job_offer.retrieval = Retrieval(
            needs=job_offer.offer_analysis.needs,
            experiences=grouped_batch
        )
        