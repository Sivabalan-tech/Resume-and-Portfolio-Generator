"""
main.py — FastAPI application entry point.

Registers all routers, configures CORS, and initializes the database on startup.
Run with: uvicorn main:app --reload --port 8000
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time

from config import APP_NAME, VERSION, ALLOWED_ORIGINS
from database import create_all_tables

# ── Import all routers ────────────────────────────────────────────────────────
from routers import auth, profile, resume, cover_letter, ats, portfolio, pdf, admin

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

# ── FastAPI App ───────────────────────────────────────────────────────────────
app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    description="🤖 AI-powered resume & portfolio builder with ATS optimization, "
                "cover letter generation, and skill gap analysis.",
    contact={"name": "Developer", "email": "dev@example.com"},
    license_info={"name": "MIT"},
    docs_url="/docs",
    redoc_url="/redoc"
)

# ── CORS Middleware ───────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request Timing Middleware ─────────────────────────────────────────────────
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000, 2)
    response.headers["X-Process-Time-Ms"] = str(duration)
    return response


# ── Startup Event ─────────────────────────────────────────────────────────────
@app.on_event("startup")
def startup_event():
    """Create database tables and log startup info."""
    logger.info(f"🚀 Starting {APP_NAME} v{VERSION}")
    create_all_tables()
    logger.info("✅ Database tables created/verified")


# ── Global Exception Handler ──────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please try again."}
    )


# ── Register Routers ──────────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(resume.router)
app.include_router(cover_letter.router)
app.include_router(ats.router)
app.include_router(portfolio.router)
app.include_router(pdf.router)
app.include_router(admin.router)


# ── Root Health Check ─────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    """Root endpoint — health check."""
    return {
        "status": "ok",
        "app": APP_NAME,
        "version": VERSION,
        "docs": "/docs"
    }


@app.get("/api/health", tags=["Health"])
def health_check():
    """Detailed health check for monitoring."""
    return {
        "status": "healthy",
        "service": APP_NAME,
        "version": VERSION
    }


@app.get("/api/test-gemini", tags=["Debug"])
def test_gemini():
    """
    Debug endpoint — tests Gemini API connection directly.
    Remove this before production deployment.
    """
    import traceback
    try:
        from services.ai_service import _call_gemini
        result = _call_gemini("Say hello in one word.")
        return {"status": "ok", "response": result}
    except Exception as e:
        return {"status": "error", "error": str(e), "traceback": traceback.format_exc()}
