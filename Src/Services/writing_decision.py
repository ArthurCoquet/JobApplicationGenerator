from Schemas.rerank_format import ExperienceEvaluation
from typing import Any
from config.settings import Settings
from Helpers.OfferRepository import OfferRepository

class WritingDecider:

    def __init__(
            self,
            settings: Settings,
            offer_repo: OfferRepository
        ) -> None:
        self.settings = settings
        self.offer_repo = offer_repo

    def get_top_experiences(self, data: list[ExperienceEvaluation]) -> list[Any]:
        """
        Trie les expériences qui ont été reranked par ordre décroissant de pertinence.
        
        Args:
            data: le dictionnaire qui contient les expériences reranked
            num_exp: le nombre d'expériences à conserver
        Returns:
            Le dictionnaire des expériences triées par ordre décroissant de pertinence et limitées au nombre d'expériences à conserver
        """
        
        return sorted(
                data,
                key=lambda experience: experience["score"],
                reverse=True
            )[:self.settings.reranking_top_k]

    def do_write(self, offer_path: str) -> tuple[bool, list[Any]]:
        """
        Indique si l'écriture du cv et de la lettre de motivation est pertinente (chaque expérience à un score suffisamment pertinent pour rédiger la lettre).

        Args:
            data: le dictionnaire des expériences triées et limitées        
        Returns:
            Booléen qui indique si la rédaction est pertinente.
        """

        data = self.offer_repo.load(offer_path)

        evaluated_experiences = self.get_top_experiences(data["rerank"]["experiences"])

        should_write = (
            len(evaluated_experiences) == self.settings.reranking_top_k
            and all(exp["score"] >= self.settings.score_threshold for exp in evaluated_experiences)
        )

        top_experiences_names = [
            exp["experience"] 
            for exp in evaluated_experiences
        ]

        #ajouter retour job_offer avec job_offer.top_experiences_names = [exp["experience"] for exp in evaluated_experiences]
        
        return should_write, top_experiences_names