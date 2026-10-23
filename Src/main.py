import asyncio

from config.settings import get_settings
from Application.build_application import build_application
from Application.pipeline import pipeline
from Schemas.job_offer import JobOffer

URL="https://www.hellowork.com/fr-fr/emplois/84208598.html?utm_source=pushOffres&utm_medium=email&utm_campaign=pushOffres&utm_term=84208598&utm_content=liste1CTA"
TITLE="---test Développeur Python - Open Prod"
CONTENT="""
Les missions du poste
Le poste :

CDI
Basé à Echirolles
39h hebdomadaires
Salaire selon compétences et expérience

Vos missions :
Intégré(e) au sein de l'équipe R&D Back-end, vous pourrez effectuer une ou plusieurs des missions suivantes :

Concevoir et développer des fonctionnalités métiers
Participer aux modifications et à l'évolution du framework Python
Participer au choix des technologies et bibliothèques de demain
Pendant votre intégration, selon vos besoins, nous vous formerons à nos outils : Python, Open-Prod, PostgreSQL, Git, ...

Le profil recherché
Vos compétences :

Formation: Bac +5 en développement ou informatique
Débutants acceptés
Maîtrise d'un langage objet
Maîtrise du SQL
Compréhension des enjeux des logiciels de gestion
Au-delà de vos compétences techniques

Vous êtes rigoureux et pragmatique
Vous montrez de l'intérêt pour les logiciels de gestion
Vous aimez collaborer sur des projets pluridisciplinaires
Vous êtes prêt à révolutionner le monde de l'industrie avec nous
"""

async def main():

    settings = get_settings()

    application = build_application(settings)

    job_offer = JobOffer(
        url=URL,
        title=TITLE,
        content=CONTENT
    )
    
    await pipeline(application=application, job_offer=job_offer)

if __name__ == "__main__":
    asyncio.run(main())