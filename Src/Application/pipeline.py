from Schemas.application import Application
from Schemas.job_offer import JobOffer    

async def pipeline(
        application: Application,
        job_offer: JobOffer
    ):    

    offer_path = rf"Offers\{job_offer.title}.json"

    application.offer_repo.save(path=offer_path, data=job_offer.model_dump())

    application.analyzer.analyze(job_offer)

    application.offer_repo.save(path=offer_path, data=job_offer.model_dump())

    await application.retriever.retrieve_experience(offer_path=offer_path)

    application.reranker.rerank_experiences(offer_path=offer_path)

    should_write, top_experiences_names = application.writing_decider.do_write(offer_path=offer_path)

    if not should_write:
        return

    application.offer_enricher.add_exp_and_facts(offer_path=offer_path, top_experiences=top_experiences_names)

    application.resume_writer.write_resume(offer_path=offer_path)

    #render resume

    application.letter_writer.write_cover_letter(offer_path=offer_path)