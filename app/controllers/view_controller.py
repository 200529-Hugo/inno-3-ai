from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse, RedirectResponse


router = APIRouter()
STATIC_DIR = Path(__file__).parent.parent / "static"


@router.get("/", include_in_schema=False)
def home() -> RedirectResponse:
    return RedirectResponse(url="/aanvraag")


@router.get("/aanvraag", include_in_schema=False)
def citizen_portal() -> FileResponse:
    return FileResponse(STATIC_DIR / "citizen.html")


@router.get("/beoordelaar", include_in_schema=False)
def reviewer_workspace() -> FileResponse:
    return FileResponse(STATIC_DIR / "reviewer.html")


@router.get("/demo", include_in_schema=False)
def dashboard() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")
