from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.controllers.api_controller import router as api_router
from app.controllers.view_controller import router as view_router
from app.database import init_database


def create_app() -> FastAPI:
    init_database()
    application = FastAPI(title="WMO AI Preparation Service", version="1.1.0")
    application.mount("/assets", StaticFiles(directory="app/static"), name="assets")
    application.include_router(view_router)
    application.include_router(api_router)
    return application


app = create_app()
