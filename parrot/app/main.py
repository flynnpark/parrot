from fastapi import FastAPI

from parrot.app.config.settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        **settings.fastapi_kwargs,
    )

    return app


app = create_app()
