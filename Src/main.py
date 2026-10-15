import asyncio

from config.settings import get_settings
from Application.build_application import build_application
from Application.pipeline import pipeline
from Schemas.job_offer import JobOffer

URL="https://fr.indeed.com/viewjob?jk=d489056336dbb5cd&tk=1k4oo6dnbjpqf801&from=jobi2a_jobmatch-reactivation-fr-FR_email&rjptk=1k4oo6cf62ct6001&xpse=SoCj67I2dgNYAUT5UJ0LbzkdCdPP&xfps=0435bf98-c28b-4d88-b9b6-dcd17befae60&xkcb=SoCp67M2dY4WYp2_MR0MbzkdCdPP"
TITLE="Data Engineer Junior - cegedim"
CONTENT="""
Description du poste
C-MEDIA, filiale du Groupe Cegedim, est l’acteur majeur de référence de la communication phygitale en pharmacie et parapharmacie :

Auprès des laboratoires pharmaceutiques par le déploiement de leur stratégie de communication sur les points de vente pharmacie
Auprès des pharmaciens en développant des solutions sur mesure et clés en main pour mettre en valeur les espaces de communication des pharmacies
Auprès des groupements de pharmacies via une offre globale pour faire vivre l’ensemble des officines de leur réseau de façon cohérente et unifiée
Par l'alliance unique de l'expertise humaine et de la puissance du digital, C-MEDIA offre des solutions 360° qui se distinguent à chaque étape du parcours du consommateur.

C-MEDIA compte plus de 250 collaborateurs et a réalisé un chiffre d’affaires de 57 millions d’euros en 2025. Pour en savoir plus : https://www.cegedim-media.fr/


Intégré au pôle Marketing & Data, vous travaillez sous la supervision d’un Chef de Projets Data, en étroite collaboration avec des interlocuteurs variés (référents métiers, équipes commerciales et techniques, pôle R&D). Votre mission principale consiste à mettre en œuvre un outil d’aide à la recommandation commerciale basée sur l’IA. Pour ce faire, vous participez à la récolte, à l’intégration et à la mise en œuvre de la chaine de structuration de la donnée relative à des campagnes publicitaires (typologies d’activations, budgets, ciblages, KPI de performance, etc.).


Les missions

Découverte et cadrage

Recueil et cartographie des sources de données existantes
Définition de la méthodologie de récolte et du schéma de données cible
Structuration de la donnée

Développement des pipelines d’extraction et de normalisation des données (extraction structurée, mapping des exports)
Définition des règles de déduplication et de réconciliation entre sources
Participation à la mise en place technique de la base de données
Intégration de la donnée

Construction du système d’intégration continue des données selon le schéma défini
Développement du prototype d’agent
Réalisation de tests avec un panel de keys users
Documentation et transfert de compétences

Documentation de l’architecture, des pipelines et du schéma des données
Participation à la formation des utilisateurs

Vous êtes issu.e d’une formation en Data Engineering et avez déjà acquis une première expérience professionnelle
Vous disposez de compétences en Python, manipulation de données (pandas), bases de données SQL (PostgreSQL apprécié) et êtes sensibles aux architectures LLM/RAG (function calling, embeddings, structured output)
Vous êtes doté.e de bonnes qualités relationnelles et êtes capable d’interagir avec des équipes non techniques (référents métiers) pour traduire un besoin utilisateur en spécifications techniques
Vous faites preuve d’autonomie et de rigueur méthodologique

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