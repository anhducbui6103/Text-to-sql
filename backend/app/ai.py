import google.generativeai as genai
from . import config
from .config import logger

def generate_sql(question: str, schema: str) -> str:
    """
    Generate a SQL SELECT query from natural language using Gemini AI.
    """
    if not config.VALID_MODEL_ID:
        return ""

    try:
        model = genai.GenerativeModel(model_name=config.VALID_MODEL_ID)

        prompt = f"""
You are a PostgreSQL expert.
Based on the schema below, write ONE SQL SELECT query.

Rules:
- Only return raw SQL
- No explanation
- No markdown

SCHEMA:
{schema}

QUESTION:
{question}

SQL:
"""
        response = model.generate_content(prompt)
        return response.text.strip() if response.text else ""

    except Exception as e:
        logger.error(f"AI Error: {e}")
        return ""
