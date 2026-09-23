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
    
    def prepare_for_rerank(
        self,
        retrieved_data: list[RetrievedExperience],
        queries: list[SearchQuery],
    ) -> dict[str, Any]:

        retrieved_data_clean: dict[str, Any] = {
            "needs": {}
        }

        # Informations sur les besoins
        for query in queries:
            retrieved_data_clean["needs"][query["name"]] = {
                "priority": query["priority"],
                "description": query["description"],
                "implicit_signals": query["implicit_signals"],
                "area": query["area"],
            }

        # Expériences et chunks
        for experience in retrieved_data:

            experience_data = {
                "categories": {}
            }

            for chunk in experience.chunks:

                # Une section peut contenir plusieurs chunks
                experience_data["categories"].setdefault(
                    chunk.section,
                    []
                )

                experience_data["categories"][chunk.section].append({
                    "chunk": chunk.content,
                    "retrieved_for": chunk.retrieved_for,
                })

            retrieved_data_clean[experience.experience] = experience_data

        return retrieved_data_clean