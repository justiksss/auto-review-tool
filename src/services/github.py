import asyncio
import base64
from enum import StrEnum

from settings import Settings
from src.interfaces.httpx import HttpxConfig
from src.models.github import GitHubFileContent
from src.services.base import BaseIntegrationService


class GitHubEndpoints(StrEnum):
    repository_content = "{owner}/{repo}/contents/{path}"


class GitHubFileTypes(StrEnum):
    file = "file"
    directory = "dir"


class AllowedFileTypes(StrEnum):
    python = ".py"
    javascript = ".js"
    typescript = ".ts"


class GitHubIntegrationService(BaseIntegrationService):
    def __init__(self, settings: Settings) -> None:
        super().__init__(
            config=HttpxConfig(
                settings.GITHUB_BASE_URL
            )
        )
        super()._set_headers(Authorization=f"Bearer {settings.GITHUB_API_KEY}",
                             Accept="application/vnd.github.v3+json")

    @staticmethod
    def get_repository_info(url: str) -> tuple[str, str]:
        """Get owner name and repository name from GitHub URL."""
        parts = url.rstrip('/').split('/')

        if len(parts) >= 2:
            return parts[-2], parts[-1]

    @staticmethod
    def decode_file_content(file: dict[str, ...]) -> str:
        return base64.b64decode(file['content']).decode() if file['type'] == GitHubFileTypes.file else None

    @staticmethod
    def is_allowed_file_type(file_name: str) -> bool:
        """Get owner name and repository name from GitHub URL."""
        return any(file_name.endswith(ext.value) for ext in AllowedFileTypes)

    async def get_repository_content(self, owner: str, repository_name: str, path: str = "") -> dict:
        return await self.get(
            uri=GitHubEndpoints.repository_content.format(owner=owner, repo=repository_name, path=path),
        )

    async def get_file_content(self, owner: str, repository_name: str, file: dict) -> GitHubFileContent:
        file_data = await self.get_repository_content(
            owner=owner, repository_name=repository_name, path=file['path']
        )

        if file_data and 'content' in file_data:
            content = self.decode_file_content(file_data)

            return GitHubFileContent(
                file_path=file['path'],
                file_name=file['name'],
                file_content=content
            )

    async def fetch_all_files(self, owner: str, repository_name: str, path: str = "") -> list[GitHubFileContent]:
        content = await self.get_repository_content(
            owner=owner, repository_name=repository_name, path=path
        )
        files_contents, tasks = list(), list()

        for file in content:
            if file['type'] == GitHubFileTypes.directory:
                tasks.append(
                    asyncio.create_task(
                        self.fetch_all_files(owner=owner, repository_name=repository_name, path=file['path']))
                )

            elif file['type'] == GitHubFileTypes.file and self.is_allowed_file_type(file['name']):
                tasks.append(
                    asyncio.create_task(self.get_file_content(owner=owner, repository_name=repository_name, file=file))
                )

        results = await asyncio.gather(*tasks)

        for result in results:
            if isinstance(result, list):
                files_contents.extend(result)
            elif result:
                files_contents.append(result)

        return files_contents
