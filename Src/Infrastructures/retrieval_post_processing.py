from qdrant_client.http.models.models import QueryResponse
from Schemas.search_query import SearchQuery
from Schemas.retrieval import RetrievedExperience, RetrievedChunk
from typing import Any

class RetrievalPostProcessing:
    def __init__(self) -> None:
         pass
    
    def parse_batch_result(
                self,
                batch_result: list[QueryResponse],
                queries_list: list[SearchQuery]
        ) -> list[dict[str, Any]]:
            
            results_parsed: list[dict[str, Any]] = []

            for query, result in zip(queries_list, batch_result):
                for point in result.points:

                    payload: dict[str, Any] = point.payload or {}

                    results_parsed.append(
                        {
                            **payload,
                            **query,
                            "score": point.score,
                        }
                    )
            return results_parsed

    def group_by_experience_and_section_and_content(
        self, results: list[dict[str, Any]]
    ) -> list[RetrievedExperience]:

        experiences: dict[str, RetrievedExperience] = {}
        chunks_index: dict[tuple[str, str, str], RetrievedChunk] = {}

        for r in results:
            exp = r["experience"]
            need = r["need"]
            section = r["section"]
            content = r["chunk"]

            if exp not in experiences:
                experiences[exp] = RetrievedExperience(
                    experience=exp,
                    chunks=[]
                )

            key = (exp, section, content)

            existing_chunk = chunks_index.get(key)

            if existing_chunk:
                if need not in existing_chunk.retrieved_for:
                    existing_chunk.retrieved_for.append(need)
            else:
                chunk = RetrievedChunk(
                    section=section,
                    content=content,
                    retrieved_for=[need],
                )

                experiences[exp].chunks.append(chunk)
                chunks_index[key] = chunk

        return list(experiences.values())
