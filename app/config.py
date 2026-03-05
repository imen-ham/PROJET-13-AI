import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    AI_PROVIDER = os.getenv("AI_PROVIDER", "mock")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")
    ANTHROPIC_MODEL = "claude-3-haiku-20240307"
    MAX_FILE_SIZE_MB = 10
    SUPPORTED_FORMATS = ["pdf", "txt", "png", "jpg", "jpeg", "webp"]
    CONFIDENCE_THRESHOLD = 0.7