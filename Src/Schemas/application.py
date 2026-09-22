from dataclasses import dataclass
from Services.offer_analyzer import OfferAnalyzer
from Services.experience_retriever import ExperienceRetriever
from Services.experience_reranker import ExperienceReranker
from Services.writing_decision import WritingDecider
from Services.offer_enricher import OfferEnricher
from Services.resume_writer import ResumeWriter
from Services.letter_writer import LetterWriter

@dataclass
class Application:
    analyzer: OfferAnalyzer
    retriever: ExperienceRetriever
    reranker: ExperienceReranker
    writing_decider: WritingDecider
    offer_enricher: OfferEnricher
    resume_writer: ResumeWriter
    letter_writer: LetterWriter