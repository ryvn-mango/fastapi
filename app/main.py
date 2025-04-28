from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings, PROJECT_NAME
from app.api.v1.endpoints import items, generate
from app.core.telemetry import setup_telemetry

app = FastAPI(
    title=PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup OpenTelemetry
setup_telemetry(app, service_name=PROJECT_NAME)

app.include_router(items.router, prefix=f"{settings.API_V1_STR}/items", tags=["items"])
app.include_router(generate.router, prefix=f"{settings.API_V1_STR}/generate", tags=["generate"]) 