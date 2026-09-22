from Infrastructures.offer_parser import saveOfferNoScrapping
from Schemas.job_offer_input import JobOfferInput
from Schemas.application import Application

async def pipeline(
        application: Application,
        job_offer: JobOfferInput
    ):

    _job_offer, offer_path = saveOfferNoScrapping(
        job_offer.content,
        job_offer.url,
        job_offer.title
    )

    application.analyzer.analyze(offer_path=offer_path)
    
    await application.retriever.retrieve_experience(offer_path=offer_path)

    application.reranker.rerank_experiences(offer_path=offer_path)

    should_write, top_experiences_names = application.writing_decider.do_write(offer_path=offer_path)

    if not should_write:
        return

    application.offer_enricher.add_exp_and_facts(offer_path=offer_path, top_experiences=top_experiences_names)

    application.resume_writer.write_resume(offer_path=offer_path)

    application.letter_writer.write_cover_letter(offer_path=offer_path)