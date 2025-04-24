from enum import StrEnum
from functools import lru_cache
from typing import Annotated, Any

from pydantic import Field
from pydantic_settings import BaseSettings


class AppEnvironment(StrEnum):
    PRODUCTION = "production"  # 프로덕션 환경
    STAGING = "staging"  # 스테이징 환경
    LOCAL = "local"  # 로컬 환경
    TEST = "test"  # 테스트(pytest) 환경


class Settings(BaseSettings):
    app_env: Annotated[AppEnvironment, Field(description="애플리케이션 환경")] = AppEnvironment.LOCAL
    disable_docs: bool = app_env == AppEnvironment.PRODUCTION

    # FastAPI
    title: str = "Parrot API"
    version: str = "0.1.0"
    debug: bool = True if app_env == AppEnvironment.LOCAL else False
    docs_url: str = "/api-docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/api-redoc"

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        kwargs: dict[str, Any] = {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }
        if self.disable_docs:
            kwargs.update(
                {
                    "docs_url": None,
                    "openapi_url": None,
                    "redoc_url": None,
                }
            )
        return kwargs


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
