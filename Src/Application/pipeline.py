from Schemas.application import Application
from Schemas.job_offer import JobOffer    

async def pipeline(
        application: Application,
        job_offer: JobOffer
    ):    

    offer_path = rf"Offers\{job_offer.title}.json"

    application.offer_repo.save(path=offer_path, data=job_offer.model_dump())

    application.analyzer.analyze(job_offer=job_offer)

    application.offer_repo.save(path=offer_path, data=job_offer.model_dump())

    await application.retriever.retrieve_experience(job_offer=job_offer)

    application.offer_repo.save(path=offer_path, data=job_offer.model_dump())

    application.reranker.rerank_experiences(job_offer=job_offer)

    application.offer_repo.save(path=offer_path, data=job_offer.model_dump())

    should_write = application.writing_decider.do_write(job_offer=job_offer)

    application.offer_repo.save(path=offer_path, data=job_offer.model_dump())

    if not should_write:
        return

    application.offer_enricher.add_exp_and_facts(job_offer=job_offer)

    application.offer_repo.save(path=offer_path, data=job_offer.model_dump())

    application.resume_writer.write_resume(job_offer=job_offer)

    application.offer_repo.save(path=offer_path, data=job_offer.model_dump())

    #render resume

    application.letter_writer.write_cover_letter_plan(job_offer=job_offer)

    application.offer_repo.save(path=offer_path, data=job_offer.model_dump())

    application.letter_writer.write_cover_letter(job_offer=job_offer)

    application.offer_repo.save(path=offer_path, data=job_offer.model_dump())


