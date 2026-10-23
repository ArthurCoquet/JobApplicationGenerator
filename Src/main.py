import asyncio

from config.settings import get_settings
from Application.build_application import build_application
from Application.pipeline import pipeline
from Schemas.job_offer import JobOffer

URL="https://www.hellowork.com/fr-fr/emplois/84575250.html"
TITLE="---test Ingénieur IA Embarquée - mercato de l'emploi"
CONTENT="""
Les missions du poste
Nous recherchons un Ingénieur IA Embarquée (H/F) - Embedded AI Engineer pour nous aider à enrichir l'écosystème existant et à en créer un nouveau pour la conduite autonome et l'IA générative.

Vos responsabilités en tant qu'Ingénieur IA/DSP comprennent la conception et l'implémentation d'algorithmes d'IA/DSP. Pour réussir dans ce poste, vous devez avoir des compétences exceptionnelles en statistiques et en programmation. Si vous avez également des connaissances en data science et en génie logiciel, nous serions ravis de vous rencontrer. Votre objectif ultime sera de concevoir et de construire des applications IA/DSP efficaces pour les produits de VSORA. Des produits qui seront utilisés par les constructeurs automobiles du monde entier et par les data-centers.



Vos missions: - Rechercher et implémenter les algorithmes et outils IA/DSP appropriés.

- Développer des applications IA/DSP temps réel sous contraintes matérielles : mémoire, consommation d'énergie, quantification.

- Réaliser un benchmarking complet par rapport à l'état de l'art correspondant.

- Effectuer des analyses statistiques et des ajustements fins à partir des résultats de tests.

- Entraîner et ré-entraîner les systèmes lorsque nécessaire.

- Étendre les bibliothèques et frameworks de ML existants.

- Rédiger des rapports techniques détaillés.

- Se tenir informé des évolutions du domaine.

Voir moins
Le profil recherché
Exigences et compétences: - Expérience avérée en tant qu'Ingénieur Machine Learning ou dans un rôle similaire

- Compréhension des structures de données, de la modélisation des données et de l'architecture logicielle

- Connaissance approfondie des mathématiques, des probabilités, des statistiques et des algorithmes

- Capacité à écrire du code robuste en Python, C, C++

- Familiarité avec les frameworks de machine learning (TensorFlow, PyTorch, OpenVINO, TVM,...) et les bibliothèques (OpenMMLab, OpenCV)

- Capacité à travailler en équipe

- Motivé et orienté objectifs

- Capacités d'analyse et de résolution de problèmes exceptionnelles

- Langues : Anglais courant (contexte international).

Serait un plus: - Expérience en traitement Radar, Lidar, Caméra, IA générative

- Expérience des plateformes ouvertes pour la conduite autonome (Apollo, Autoware)

- Expérience du déploiement en data-center

- Master en informatique, Machine Learning / IA ou domaine similaire ; Doctorat

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