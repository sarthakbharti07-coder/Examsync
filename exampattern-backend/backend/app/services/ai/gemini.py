from google import genai

from app.core.config import settings


class GeminiService:
    def __init__(self):
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is missing from .env")

        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.gemini_model

    def generate_response(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        if not response.text:
            raise RuntimeError("Gemini returned an empty response")

        return response.text


gemini_service = GeminiService()
