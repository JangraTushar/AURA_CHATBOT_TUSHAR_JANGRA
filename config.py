# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# LLM config (Groq)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"

# Vector DB config
CHROMA_DB_DIR = "./chroma_db"

# Files
KB_FILE = "agricultural_knowledge_base.json"
SAMPLE_FARM_DATA_FILE = "sample_farm_data.json"
DIAGNOSTIC_RULES_FILE = "diagnostic_rules.json"
