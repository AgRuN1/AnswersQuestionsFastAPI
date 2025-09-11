import uvicorn
from fastapi import FastAPI
from app.routes import get_apps_router
from app.config.settings import project_settings
from app.middlewares.logger import LoggerMiddleware


def get_application() -> FastAPI:
    application = FastAPI(
        title=project_settings.PROJECT_NAME,
        debug=project_settings.DEBUG,
        version=project_settings.VERSION
    )
    application.include_router(get_apps_router())
    application.add_middleware(LoggerMiddleware)

    return application


app = get_application()


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=80, reload=True)
