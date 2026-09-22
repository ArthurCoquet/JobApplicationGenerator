import asyncio

from config.settings import get_settings
from Application.build_application import build_application
from Application.pipeline import pipeline
from Schemas.job_offer_input import JobOfferInput

URL="https://www.hellowork.com/fr-fr/emplois/80062195.html"
TITLE="Data Analyst - Audensiel Technologies"
CONTENT="""
Les missions du poste
Dans le cadre du développement de notre gouvernance des données et de la modernisation de nos outils de pilotage, nous renforçons nos équipes techniques en recrutant un(e ) Data Analyst, expert(e) en technologies SQL et Power BI.

Le profil recherché
Sous la responsabilité du Responsable de la Business Intelligence, le/la Data Analyst aura pour mission principale de structurer les données de l'organisation et de concevoir les outils d'aide à la décision à destination des directions métiers.

À ce titre, vos fonctions se déclinent comme suit :

Collecte et modélisation des données : Concevoir, optimiser et exécuter des requêtes SQL complexes pour extraire, nettoyer et consolider les données issues de nos différents systèmes d'information (ERP, CRM, Data Warehouse).
Développement de solutions décisionnelles : Concevoir, réaliser et maintenir les tableaux de bord et rapports dynamiques sous Power BI, en veillant à la pertinence des indicateurs (KPIs) et à la qualité visuelle des livrables.
Analyse de performance : Produire des analyses statistiques et des notes de synthèse pour éclairer les choix stratégiques et opérationnels de la direction.
Accompagnement au changement : Assurer la maintenance évolutive des rapports existants, rédiger la documentation technique et fonctionnelle, et animer des sessions de formation pour accompagner la montée en compétences des utilisateurs finaux (Data Literacy).

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