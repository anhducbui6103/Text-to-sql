"""
Evaluation module for ViText2SQL dataset
Uses tables.json for schema (no need for SQLite database file)
"""
import json
import re
import time
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, asdict

import google.generativeai as genai
from dotenv import load_dotenv
import os


@dataclass
class EvalResult:
    """Single evaluation result"""
    db_id: str
    question: str
    gold_sql: str
    pred_sql: str
    sql_valid: bool = False  # SQL parses/runs
    select_only: bool = False  # Only SELECT queries
    em_match: bool = False  # Exact Match (normalized SQL)
    ex_match: bool = False  # Execution match (results match)
    pred_error: Optional[str] = None
    gold_error: Optional[str] = None
    gen_time: float = 0.0


class SchemaLoader:
    """Load schema từ tables.json (không cần SQLite database)"""
    
    def __init__(self, tables_json_path: Path):
        """
        Args:
            tables_json_path: Path to tables.json from Spider
        """
        self.tables_json_path = Path(tables_json_path).resolve()
        if not self.tables_json_path.exists():
            raise FileNotFoundError(f"tables.json not found: {self.tables_json_path}")
        
        # Load all tables
        with self.tables_json_path.open("r", encoding="utf-8") as f:
            self.all_tables = json.load(f)
        
        # Build index by db_id
        self.db_index = {}
        for idx, table_info in enumerate(self.all_tables):
            db_id = table_info.get("db_id")
            if db_id:
                self.db_index[db_id] = idx
    
    def get_schema(self, db_id: str) -> str:
        """Extract schema as formatted text"""
        if db_id not in self.db_index:
            return f"# Database {db_id} not found in tables.json"
        
        table_info = self.all_tables[self.db_index[db_id]]
        table_names = table_info.get("table_names", [])
        column_names = table_info.get("column_names", [])
        column_types = table_info.get("column_types", [])
        
        lines = []
        for table_idx, table_name in enumerate(table_names):
            lines.append(f"Table {table_name}:")
            
            # Get columns for this table
            for col_list, col_type in zip(column_names, column_types):
                if len(col_list) >= 2:
                    col_table_idx, col_name = col_list[0], col_list[1]
                    if col_table_idx == table_idx:
                        col_type_str = col_type if col_type else "TEXT"
                        lines.append(f"  - {col_name} ({col_type_str})")
        
        return "\n".join(lines) if lines else f"# No schema info for {db_id}"


class GeminiSQLGenerator:
    """Generate SQL from questions using Gemini"""
    
    def __init__(self, model_name: Optional[str] = None):
        """
        Args:
            model_name: Gemini model name (auto-select if None)
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY env var not set")
        
        genai.configure(api_key=api_key)
        
        if model_name:
            self.model_name = model_name
        else:
            self.model_name = self._select_model()
    
    def _select_model(self) -> str:
        """Auto-select best available Gemini model"""
        models = [m.name for m in genai.list_models() 
                 if "generateContent" in getattr(m, "supported_generation_methods", [])]
        
        priority = [
            "models/gemini-2.5-flash",
            "models/gemini-2.5-pro",
            "models/gemini-2.0-flash",
            "models/gemini-flash-latest",
            "models/gemini-pro-latest",
        ]
        
        for p in priority:
            if p in models:
                return p
        
        gemini_models = [m for m in models if "gemini" in m]
        if gemini_models:
            return gemini_models[0]
        
        raise RuntimeError("No Gemini generateContent model available")
    
    def generate(self, question: str, schema: str) -> str:
        """Generate SQL from question + schema"""
        prompt = f"""You are a SQLite expert.
Based on the schema below, write ONE SQL SELECT query.

Rules:
- Only return raw SQL
- No explanation
- No markdown
- Use SQLite-compatible syntax
- Do NOT add `;` at the end

SCHEMA:
{schema}

QUESTION (in Vietnamese):
{question}

SQL:
""".strip()
        
        try:
            model = genai.GenerativeModel(model_name=self.model_name)
            resp = model.generate_content(prompt)
            sql = resp.text if resp and resp.text else ""
            return self._normalize_sql(sql)
        except Exception as e:
            raise RuntimeError(f"Gemini generation error: {e}")
    
    @staticmethod
    def _normalize_sql(sql: str) -> str:
        """Normalize SQL string"""
        if not sql:
            return ""
        sql = sql.strip()
        # Remove markdown code blocks
        sql = re.sub(r"^```.*\n", "", sql)
        sql = re.sub(r"\n```$", "", sql)
        # Remove 'sql' prefix
        sql = re.sub(r"^sql\s+", "", sql, flags=re.IGNORECASE).strip()
        # Remove trailing semicolon
        sql = sql.rstrip(";").strip()
        return sql


class ViTextEvaluator:
    """Main evaluator: ViText2SQL dataset using tables.json for schema"""
    
    def __init__(self, tables_json_path: Path, model_name: Optional[str] = None):
        """
        Args:
            tables_json_path: Path to tables.json from Spider
            model_name: Gemini model name (auto-select if None)
        """
        self.schema_loader = SchemaLoader(tables_json_path)
        self.generator = GeminiSQLGenerator(model_name)
    
    @staticmethod
    def normalize_sql_for_em(sql: str) -> str:
        """Normalize SQL for Exact Match comparison"""
        sql = sql.lower().strip()
        # Remove extra spaces
        sql = re.sub(r'\s+', ' ', sql)
        sql = sql.rstrip(";")
        return sql
    
    def eval_single(self, db_id: str, question: str, gold_sql: str) -> EvalResult:
        """Evaluate single sample - MOCK execution (no DB needed)"""
        result = EvalResult(
            db_id=db_id,
            question=question,
            gold_sql=gold_sql,
            pred_sql=""
        )
        
        # Get schema
        schema = self.schema_loader.get_schema(db_id)
        if not schema or schema.startswith("#"):
            result.pred_error = f"Schema not found for db_id={db_id}"
            return result
        
        # Generate SQL
        t0 = time.time()
        try:
            pred_sql = self.generator.generate(question, schema)
            result.gen_time = time.time() - t0
            result.pred_sql = pred_sql
        except Exception as e:
            result.pred_error = str(e)
            return result
        
        # Check if SELECT-only
        result.select_only = pred_sql.upper().startswith("SELECT")
        
        # For now: mark as "valid" if SELECT-only (no actual execution)
        # Future: can add mock execution or use LLM-as-judge
        if result.select_only:
            result.sql_valid = True
        else:
            result.pred_error = "Not a SELECT statement"
            result.sql_valid = False
        
        # Exact Match (normalized SQL)
        pred_norm = self.normalize_sql_for_em(pred_sql)
        gold_norm = self.normalize_sql_for_em(gold_sql)
        result.em_match = pred_norm == gold_norm
        
        # Note: EX (Execution Accuracy) cannot be computed without actual DB
        # Set to same as EM as proxy (or implement mock comparison)
        result.ex_match = result.em_match
        
        return result


def load_vitext2sql_split(split: str = "test", limit: Optional[int] = None) -> list:
    """Load ViText2SQL split from HuggingFace"""
    from datasets import load_dataset
    
    ds = load_dataset("SEACrowd/vitext2sql", split=split, trust_remote_code=True)
    
    samples = []
    n = min(limit, len(ds)) if limit else len(ds)
    
    for i in range(n):
        ex = ds[i]
        samples.append({
            "db_id": ex.get("db_id"),
            "question": ex.get("question"),
            "gold_sql": ex.get("query"),  # ViText2SQL uses 'query' field
        })
    
    return samples
