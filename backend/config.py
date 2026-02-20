"""
Configuration settings loaded from environment variables.
Uses python-dotenv to load .env file in development.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ─── JWT Settings ─────────────────────────────────────────────────────────────
SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production-please")
ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# ─── AI ───────────────────────────────────────────────────────────────────────
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# ─── Database ─────────────────────────────────────────────────────────────────
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./resume_builder.db")

# ─── App ──────────────────────────────────────────────────────────────────────
APP_NAME: str = "AI Resume & Portfolio Builder"
VERSION: str = "1.0.0"
ALLOWED_ORIGINS: list = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://your-vercel-app.vercel.app",  # replace with actual URL on deploy
]
