from Helpers.OfferRepository import OfferRepository
from config.settings import Settings
from Schemas.job_offer import JobOffer

class OfferEnricher:

    def __init__(
            self,
            settings: Settings,
            offer_repo: OfferRepository
    ) -> None:

        self.settings= settings
        self.offer_repo = offer_repo

    def add_exp_and_facts(self, job_offer: JobOffer) -> None:

        experiences = self.offer_repo.load(self.settings.complete_experiences_filepath)
        personal_facts = self.offer_repo.load(self.settings.personal_facts_filepath)

        job_offer.personal_facts = personal_facts

        if job_offer.top_experiences_names is None:
            raise ValueError("top_experiences_names has not been computed yet.")

        for name in job_offer.top_experiences_names:
            if name in experiences:
                setattr(job_offer, name, experiences[name])

