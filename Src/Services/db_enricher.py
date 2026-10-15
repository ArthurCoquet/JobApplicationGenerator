
import asyncio
import json
import sys
from pathlib import Path

# Ajouter la racine Src au chemin de recherche Python
SRC_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SRC_ROOT))

from Infrastructures.vector_db import VectorStoreIndexer
from config.settings import get_settings


settings = get_settings()
vs_indexer = VectorStoreIndexer()


with open(r"Docs\expeerience_jobsearch.json", "r", encoding="utf-8") as f:
    docs = json.load(f)


async def main():
    await vs_indexer.index_documents(
        collection_name=settings.qdrant_collection,
        docs=docs,
    )


if __name__ == "__main__":
    asyncio.run(main())
