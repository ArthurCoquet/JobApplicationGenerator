from Helpers.OfferRepository import OfferRepository
from config.settings import Settings

class OfferEnricher:

    def __init__(
            self,
            settings: Settings,
            offer_repo: OfferRepository
    ) -> None:

        self.settings= settings
        self.offer_repo = offer_repo

    def add_exp_and_facts(self, offer_path: str, top_experiences: list[str]) -> None:

        data = self.offer_repo.load(offer_path)
        experiences = self.offer_repo.load(self.settings.complete_experiences_filepath)
        personal_facts = self.offer_repo.load(self.settings.personal_facts_filepath)

        for k, v in experiences.items():
            if k in top_experiences:
                data[k] = v

        data["personal_facts"] = personal_facts

        self.offer_repo.save(path=offer_path, data=data)