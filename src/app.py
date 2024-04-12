from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.config import Settings
from src.routes.tasks import task_router
from src.routes.users import users_router

def main_app():
    settings = Settings.get_settings()
    origins = settings.cors_origins.split(",") if settings.cors_origins else []

    #Create the FastAPI application
    app = FastAPI(root_path=settings.base_path)

    #Add middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=settings.allowed_methods,
        allow_headers=["*"]
    )

    #Add routes for the application
    app.include_router(task_router)
    app.include_router(users_router)

    return app
