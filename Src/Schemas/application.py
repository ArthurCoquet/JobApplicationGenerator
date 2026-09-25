from dataclasses import dataclass
from Helpers.OfferRepository import OfferRepository
from Services.offer_analyzer import OfferAnalyzer
from Services.experience_retriever import ExperienceRetriever
from Services.experience_reranker import ExperienceReranker
from Services.writing_decision import WritingDecider
from Services.offer_enricher import OfferEnricher
from Services.render_resume import ResumeRenderer
from Services.resume_writer import ResumeWriter
from Services.letter_writer import LetterWriter

@dataclass
class Application:
    offer_repo: OfferRepository
    analyzer: OfferAnalyzer
    retriever: ExperienceRetriever
    reranker: ExperienceReranker
    writing_decider: WritingDecider
    offer_enricher: OfferEnricher
    resume_renderer: ResumeRenderer
    resume_writer: ResumeWriter
    letter_writer: LetterWriter