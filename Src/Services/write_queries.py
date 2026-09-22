from Schemas.job_offer import JobOffer
from Schemas.search_query import SearchQuery

def write_queries(job_offer: JobOffer) -> list[SearchQuery]:
    """
    Construit les requêtes de recherche utilisées pour interroger le vectorstore
    à partir des besoins extraits de l'analyse de l'offre d'emploi.

    Args:
        job_offer: structure contenant l'analyse structurée de l'offre d'emploi.

    Returns:
        list[SearchQuery]:
            Liste des requêtes de recherche générées à partir des besoins
            identifiés dans l'offre. Chaque requête contient :
            - la requête textuelle utilisée pour le retrieval
            - le besoin associé
            - sa description
            - les signaux implicites
            - sa priorité
            - son domaine d'impact
    """

    if job_offer.offer_analysis is None:
        raise ValueError("offer_analysis has not been computed yet")

    needs = job_offer.offer_analysis.needs

    queries: list[SearchQuery] = []
    
    for need in needs:

        query_parts = [
            need.name,
            need.description,
            *need.implicit_signals
        ]

        query = " ".join(query_parts)

        queries.append({
            "query": query,
            "name": need.name,
            "need": need.name,
            "description": need.description,
            "implicit_signals": need.implicit_signals,
            "priority": need.priority,
            "area": need.impact_area
        })
    
    return queries
