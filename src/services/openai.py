from openai import AsyncOpenAI

from settings import Settings
from src.interfaces.httpx import HttpxConfig
from src.models.github import GitHubFileContent
from src.models.openai import OpenAIResultEntity
from src.services.base import BaseIntegrationService


class OpenAIIntegrationService(BaseIntegrationService):
    def __init__(self, settings: Settings) -> None:
        super().__init__(
            config=HttpxConfig(
                settings.OPENAI_BASE_URL
            )
        )

        self.openai = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    @staticmethod
    def construct_prompt(files: list[GitHubFileContent]) -> str:
        """Constructs a prompt to send to OpenAI API for evaluation."""

        prompt = "You are reviewing a repository with the following files:\n\n"

        for file in files[:1]:
            prompt += f"File: {file.file_name}\n"
            prompt += f"Content:\n{file.file_content[:5]}\n"  # Limit content to first 1000 characters
            prompt += "...\n\n"

        prompt += "Please provide:\n1. A rating of the repository from 1 to 10.\n"
        prompt += "2. A conclusion about the quality of the repository.\n"
        return prompt

    @staticmethod
    def parse_openai_response(response: str) -> OpenAIResultEntity:
        if response is None:
            return OpenAIResultEntity()

        lines = response.splitlines()

        rating, conclusion = None, None

        for line in lines:
            if "Rating:" in line:
                rating = line.split("Rating:")[-1].strip()
            elif "Conclusion:" in line:
                conclusion = line.split("Conclusion:")[-1].strip()

        return OpenAIResultEntity(rating=rating, conclusion=conclusion)

    async def query_openai(self, files: list[GitHubFileContent]) -> str:
        prompt = self.construct_prompt(files)

        try:
            response = await self.openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400_000,  # Adjust based on your needs
            )
            return response['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"Error querying OpenAI: {e}")

    async def get_repository_report(self, files: list[GitHubFileContent]) -> OpenAIResultEntity:
        openai_result = await self.query_openai(files=files)

        return self.parse_openai_response(openai_result)
