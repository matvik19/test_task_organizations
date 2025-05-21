import subprocess

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.routres import all_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    subprocess.run("alembic upgrade head", shell=True, check=True)
    yield


app = FastAPI(
    title="API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)
api = APIRouter(
    prefix="/api",
    responses={404: {"description": "Page not found"}},
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

for router in all_routers:
    api.include_router(router)

app.include_router(api)
