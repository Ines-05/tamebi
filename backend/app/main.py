from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routes.shorten import router as shorten_router
from app.routes.redirect import router as redirect_router
from app.routes.analytics import router as analytics_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 URL Shortener API started")
    yield
    print("🛑 URL Shortener API stopped")


app = FastAPI(
    title="URL Shortener API",
    description="Shorten URLs with auto-generated or custom aliases",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite and common React ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", tags=["Health"])
@app.get("/health", tags=["Health"])  # Keep both for flexibility
async def health_check():
    return {"status": "ok"}


app.include_router(shorten_router, prefix="/api", tags=["Shortener"])
app.include_router(analytics_router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(redirect_router, tags=["Redirect"])  # catch-all /{alias} — must be last