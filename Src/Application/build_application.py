from config.settings import Settings
from Infrastructures.llm_inference import LlmInference
from Infrastructures.vector_search import VectorSearch
from Infrastructures.retrieval_post_processing import RetrievalPostProcessing
from Services.offer_analyzer import OfferAnalyzer
from Services.experience_retriever import ExperienceRetriever
from Services.experience_reranker import ExperienceReranker
from Services.writing_decision import WritingDecider
from Services.offer_enricher import OfferEnricher
from Services.resume_writer import ResumeWriter
from Services.letter_writer import LetterWriter
from Helpers.OfferRepository import OfferRepository
from Schemas.application import Application

def build_application(
        settings: Settings
) -> Application :
    
    offer_repo = OfferRepository()

    llm = LlmInference(settings=settings)

    analyzer = OfferAnalyzer(
        llm=llm,
        settings=settings
    )

    post_processing = RetrievalPostProcessing()

    vector_search = VectorSearch(
        settings=settings,
        post_processing=post_processing
    )

    retriever = ExperienceRetriever(
        settings=settings,
        vector_search=vector_search
    )

    reranker = ExperienceReranker(
        llm=llm, 
        settings=settings
    )

    writing_decider = WritingDecider(
        settings=settings,
    )

    offer_enricher = OfferEnricher(
        settings=settings,
        offer_repo=offer_repo
    )

    resume_writer = ResumeWriter(
        llm=llm,
        settings=settings
    )

    letter_writer = LetterWriter(
        llm=llm, 
        settings=settings
    )

    return Application(
        offer_repo=offer_repo,
        analyzer=analyzer,
        retriever=retriever,
        reranker=reranker,
        writing_decider=writing_decider,
        offer_enricher=offer_enricher,
        resume_writer=resume_writer,
        letter_writer=letter_writer
    )