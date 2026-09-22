import asyncio

from config.settings import get_settings
from Application.build_application import build_application
from Application.pipeline import pipeline
from Schemas.job_offer_input import JobOfferInput

URL="https://www.welcometothejungle.com/fr/companies/ministere-des-armees-fr/jobs/data-analyst_merignac"
TITLE="Data Analyst - TEST - Civils de la Défense - Ministère des Armées et des Anciens combattants"
CONTENT="""
Vos missions en quelques mots

Le Data Analyst est un acteur de premier plan dans la collecte, l’analyse, l’interprétation et la présentation des données permettant d’orienter les décisions stratégiques du CTAAE. Placé sous la responsabilité hiérarchique du chef de la division data, vous serez en contact permanent avec le commandement du CTAAE, les référents métier et les spécialistes data du centre numérique de la donnée (CNDAAE) de Mont-de-Marsan.
Votre principale mission sera d’analyser et d’interpréter les données afin d’en extraire des informations pertinentes pour guider les stratégies des opérationnels et des référents métier. Dans ce cadre,

Vous collecterez et structurerez les données issues de différentes sources ;
Vous analyserez les données pour identifier des tendances et des opportunités ;
Vous créerez des rapports et des tableaux de bord interactifs ;
Vous collaborerez avec les équipes métier pour définir leurs besoins en données ;
Vous participerez à des projets de transformation digitale impliquant la donnée ;
Vous assurerez la qualité et la sécurité des données analysées.

Profil recherché
Profil recherché

Issu d’une formation d’un bac+5 ou équivalent dans le domaine de l’informatique, des systèmes d’information ou de la donnée, vous justifiez d’une expérience professionnelle dans le domaine de la collecte, l’analyse, l’interprétation et la présentation des données.
Vous possédez de bonnes connaissances dans la mise en œuvre et l’utilisation des outils et méthodes pour organiser, synthétiser et valoriser les données pour aider les décideurs dans leur prise de décision. Vous avez une compétence avérée à travailler en équipe et en mode projet (proactif, rigoureux, méthodique) avec une forte adaptabilité. Enfin, votre capacité à être force de proposition et votre sens de l’engagement sont indispensables à la réalisation des missions de votre poste.
"""

async def main():

    settings = get_settings()

    application = build_application(settings)

    job_offer = JobOfferInput(
        url=URL,
        title=TITLE,
        content=CONTENT
    )
    
    await pipeline(application=application, job_offer=job_offer)

if __name__ == "__main__":
    asyncio.run(main())