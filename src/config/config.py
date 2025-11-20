import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class"""
    
    # PostgreSQL
    POSTGRES_USER = os.getenv("POSTGRES_USER", "flaskuser")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "flaskpass")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "flaskdb")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    
    # Database URL
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Ollama
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:4b")
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434") # Inside docker network use "http://ollama:11434", from host use "http://localhost:11435"
    OLLAMA_HOST_PORT = os.getenv("OLLAMA_HOST_PORT", "11435")
    OLLAMA_CONTAINER_PORT = os.getenv("OLLAMA_CONTAINER_PORT", "11434")
    OLLAMA_MODELS_PATH = os.getenv("OLLAMA_MODELS_PATH", "/root/.ollama/models")
    
    # Flask
    FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    
    # Adminer
    ADMINER_PORT = os.getenv("ADMINER_PORT", "8080")
    
    # Upload folder
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
