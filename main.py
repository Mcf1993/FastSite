from app.core.exceptions import http_exception_handler, params_validation_handler
from app.core.routers import api_routers
from app.core.settings import settings
from app.db.postgresql import SessionLocal
from fastapi import FastAPI, Request, Response
from fastapi.exceptions import HTTPException, RequestValidationError
from dotenv import load_dotenv

load_dotenv(verbose=True)


app = FastAPI(
    title=settings.TITLE,
    version=settings.VERSION,
    debug=settings.DEBUG,
    docs_url=settings.DOCS_URL if settings.DEBUG else None,
    redoc_url=settings.DOCUMENTATION_URL if settings.DEBUG else None
)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, params_validation_handler)
app.include_router(api_routers)


@app.middleware('http')
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response
