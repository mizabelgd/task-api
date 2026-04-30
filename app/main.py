from contextlib import asynccontextmanager
from datetime import datetime, timezone

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.router import router as v1_router
from app.db.base import Base
from app.db.session import engine
import app.models.task  # noqa: F401
import app.models.user  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="task-api", version="0.3.0", lifespan=lifespan)
app.include_router(v1_router)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "type": f"https://httpstatuses.com/{exc.status_code}",
            "title": exc.detail if isinstance(exc.detail, str) else "HTTP Error",
            "status": exc.status_code,
            "detail": exc.detail,
            "instance": request.url.path,
        },
        headers=getattr(exc, "headers", None),
        media_type="application/problem+json",
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "type": "https://httpstatuses.com/422",
            "title": "Validation Error",
            "status": 422,
            "detail": exc.errors(),
            "instance": request.url.path,
        },
        media_type="application/problem+json",
    )


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
