import asyncio
import json
import sys
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SRC_ROOT))

from Infrastructures.vector_db import VectorStoreIndexer
from config.settings import get_settings
from Schemas.experiences import Experiences, Experience


settings = get_settings()
vs_indexer = VectorStoreIndexer()

with open(r"Docs\experiences_chunks.json", "r", encoding="utf-8") as f:
    docs = json.load(f)

result = Experiences(experiences=[Experience(**experience) for experience in docs["experiences"]])

async def main():
    await vs_indexer.index_documents(
        collection_name=settings.qdrant_collection,
        docs=result,
    )

if __name__ == "__main__":
    asyncio.run(main())
