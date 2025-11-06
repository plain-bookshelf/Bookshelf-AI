import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

OLLAMA_MODEL = "exaone3.5:latest"
GEMINI_MODEL = "gemini-2.5-flash"
EMBED_MODEL = "jhgan/ko-sroberta-multitask"

KEY=os.getenv("GOOGLE_KEY")
