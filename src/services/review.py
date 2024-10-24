from src.models.review import ReviewResponseEntityModel
from src.services.base import BaseService
from src.services.cache import CacheService
from src.services.github import GitHubIntegrationService
from src.services.openai import OpenAIIntegrationService
from web.http.v1.routers.review.schemas.body import ReviewBody


class ReviewService(BaseService):
    def __init__(self, github_service: GitHubIntegrationService, openai_service: OpenAIIntegrationService,
                 cache_service: CacheService) -> None:
        self.github_service = github_service
        self.openai_service = openai_service
        self.cache_service = cache_service

    async def get_review(self, schema: ReviewBody) -> ReviewResponseEntityModel:
        repository_owner, repository_name = self.github_service.get_repository_info(str(schema.github_repo_url))

        async with self.github_service.async_client:
            files_content = await self.cache_service.get_record(
                cache_key=str(schema.github_repo_url)
            )

            if files_content is None:  # not found in cache
                files_content = await self.github_service.fetch_all_files(
                    owner=repository_owner, repository_name=repository_name
                )
                await self.cache_service.create_record(cache_key=str(schema.github_repo_url),
                                                       data=[file.model_dump(mode="json") for file in files_content])

            openai_response = await self.openai_service.get_repository_report(
                files=files_content
            )

            return ReviewResponseEntityModel(
                found_files=files_content,
                **openai_response.model_dump()
            )


