#Code from https://build.nvidia.com/nvidia/nemotron-3-super-120b-a12b
from openai import OpenAI
import logging
from pydantic import BaseModel
from config.settings import Settings
from typing import TypeVar

T = TypeVar("T", bound=BaseModel)

logger = logging.getLogger(__name__)


class LlmInference:
    def __init__(
        self,
        settings: Settings,
        temperature: float = 0.7,
        top_p: float = 0.9,
    ) -> None:
        """
        Initialise le client LLM et charge le prompt système.

        Args:
            base_url: endpoint de l’API 
            api_key: clé API 
            model: nom du modèle à utiliser
            temperature: contrôle de la créativité du modèle
            top_p: contrôle du sampling nucleus
        """
        self.client = OpenAI(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key
        )

        self.model = settings.llm_model
        self.temperature = temperature
        self.top_p = top_p

        logger.info(
            "LlmInference initialisé (model=%s, base_url=%s)",
            self.model,
            settings.llm_base_url
        )


    def load_system_prompt(self, path: str) -> str:
        """
        Charge le prompt système depuis un fichier texte.

        Raises:
            FileNotFoundError: si le fichier n'existe pas
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            logger.error("System prompt introuvable: %s", path)
            raise

    def generate_structured_response(self, content: str, response_format: type[T], system_prompt_path: str) -> T:
        """
        Effectue un appel au LLM avec le prompt système + message utilisateur. Utilise le format JobAnalysisResponse
        """
        system_prompt = self.load_system_prompt(system_prompt_path)

        try:
            completion = self.client.chat.completions.parse(
                model=self.model,
                messages=[{"role": "system", "content": system_prompt}, {"role":"user","content":content}],
                temperature=self.temperature,
                top_p=self.top_p,
                response_format=response_format
            )
        except Exception:
            logger.exception("Erreur lors de l'appel au LLM")
            raise

        usage = completion.usage

        if usage:
            logger.info(
                "LLM usage: prompt=%s, cached=%s, completion=%s",
                usage.prompt_tokens,
                usage.prompt_tokens_details.cached_tokens if usage.prompt_tokens_details else None,
                usage.completion_tokens,
            )

        message = completion.choices[0].message 
        if message.parsed:
            return message.parsed
        raise ValueError("LLM did not return a response.")
