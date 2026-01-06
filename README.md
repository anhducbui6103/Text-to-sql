# Vietnamese Text-to-SQL Assistant 🤖

Convert natural language Vietnamese questions into SQL queries using AI. A practical demonstration of combining LLM with database systems.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

## 📋 Overview

**AI Text-to-SQL** is a system that:

1. **Accepts Vietnamese questions** from users
2. **Analyzes database schema** automatically
3. **Generates SQL queries** using Gemini AI
4. **Executes queries** on PostgreSQL
5. **Returns results** as JSON to frontend

Perfect for:
- 📚 Learning AI + Database integration
- 🎓 Teaching SQL and Backend concepts
- 🏢 Building data access layers
- 🚀 Creating internal tools and dashboards

> **Technology Stack**: FastAPI + Gemini API + PostgreSQL + Docker + Vue-like Frontend

---

## ✨ Features

### Core Features
- ✅ **Vietnamese NLP Support** - Understands Vietnamese questions
- ✅ **AI-Powered SQL Generation** - Uses Google Gemini 2.5 Flash
- ✅ **Real-time Database Execution** - Direct PostgreSQL integration
- ✅ **REST API** - Easy integration with any frontend
- ✅ **Docker Ready** - One-command deployment

### Development Features
- ✅ **Evaluation Framework** - Measure model accuracy
- ✅ **Results Analysis** - Understand error patterns
- ✅ **Metrics Tracking** - SQL validity, exact match, execution accuracy
- ✅ **Schema Handling** - Automatic database introspection

### Frontend Features
- 🎨 **Modern Web UI** - Clean, responsive interface
- 📊 **Query History** - Stores previous queries
- 🎯 **Auto-complete** - Schema suggestions
- 💾 **Results Export** - Download as JSON/CSV
- 🌙 **Dark Mode** - Eye-friendly theme

---

## 🏗️ Architecture

### System Flow

```
┌─────────────────┐
│   Frontend UI   │
│  (HTML/JS)      │
└────────┬────────┘
         │ POST /api/query
         │ { question: "..." }
         ▼
┌─────────────────┐
│  FastAPI Server │
│  (Backend)      │
├─────────────────┤
│ • Parse request │
│ • Get DB schema │
│ • Call AI API   │
│ • Validate SQL  │
│ • Execute query │
└────────┬────────┘
         │ Generated SQL
         ▼
┌─────────────────┐
│   PostgreSQL    │
│   Database      │
└─────────────────┘
```

### Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Backend** | FastAPI | 0.115.0 |
| **Web Server** | Uvicorn | 0.30.6 |
| **Database** | PostgreSQL | 16 |
| **ORM** | SQLAlchemy | 2.0 |
| **AI API** | Gemini | 2.5 Flash |
| **Containerization** | Docker Compose | Latest |
| **Frontend** | HTML5/CSS3/JS | Vanilla |

---

## 🚀 Quick Start

### Prerequisites

- **Docker** and **Docker Compose** installed
- **Gemini API Key** (get from [ai.google.dev](https://ai.google.dev))
- **Python 3.9+** (for evaluation scripts)

### 1. Clone & Setup

```bash
git clone <repository-url>
cd AI-Text-To-SQL-main
```

### 2. Configure Environment

Create `.env` file in `backend/` folder:

```env
GEMINI_API_KEY=your_api_key_here
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/sql_demo
```

### 3. Start Services

```bash
docker compose up --build
```

Expected output:
```
✓ PostgreSQL service running on :5432
✓ Backend service running on :8000
✓ Frontend available at http://localhost:80
```

### 4. Access the Application

- **Frontend**: http://localhost (or open `frontend/index.html`)
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

---

## 📖 Usage

### Via Frontend Web UI

1. Open http://localhost in your browser
2. Type Vietnamese question in input box
3. View generated SQL and results
4. Browse query history

### Via API (cURL)

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Liệt kê tên và email của nhân viên?"
  }'
```

### Via Python

```python
import requests

response = requests.post(
    "http://localhost:8000/api/query",
    json={"question": "Tổng số nhân viên?"}
)

print(response.json())
# {
#   "success": true,
#   "question": "Tổng số nhân viên?",
#   "sql_generated": "SELECT COUNT(*) FROM nhan_vien;",
#   "results": [{"COUNT(*)": 150}],
#   "execution_time": 0.042
# }
```

---

## 🔌 API Reference

### POST /api/query

Convert natural language to SQL and execute.

**Request:**
```json
{
  "question": "Vietnamese natural language question"
}
```

**Response (Success):**
```json
{
  "success": true,
  "question": "Input question",
  "sql_generated": "SELECT ... FROM ...",
  "results": [
    {"column1": "value1", "column2": "value2"}
  ],
  "execution_time": 0.123
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Error description",
  "details": "Additional details if available"
}
```

### GET /api/health

Check if API is running.

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "ai_model": "models/gemini-2.5-flash"
}
```

### GET /api/schema

Get database schema information.

**Response:**
```json
{
  "tables": [
    {
      "name": "nhan_vien",
      "columns": [
        {"name": "id", "type": "INTEGER"},
        {"name": "name", "type": "VARCHAR"}
      ]
    }
  ]
}
```

---

## 📁 Project Structure

```
AI-Text-To-SQL-main/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app & lifespan handler
│   │   ├── routes.py            # API endpoints
│   │   ├── ai.py                # SQL generation logic
│   │   ├── database.py          # PostgreSQL connection
│   │   ├── config.py            # Configuration
│   │   ├── schemas.py           # Pydantic models
│   │   └── utils.py             # Helper functions
│   ├── eval/
│   │   ├── __init__.py
│   │   ├── eval.py              # Core evaluation framework
│   │   ├── README.md
│   │   └── outputs/             # Evaluation results
│   ├── Dockerfile
│   └── requirements.txt          # Python dependencies
├── frontend/
│   ├── index.html               # Web UI
│   ├── script.js                # Client logic
│   ├── style.css                # Styling
│   └── logo.jpg
├── scripts/
│   ├── eval_vitext2sql.py       # Run evaluation on ViText2SQL
│   ├── analyze_results.py       # Analyze eval results
│   └── prepare_training_data.py # (Optional) Prepare fine-tuning data
├── docker-compose.yml           # Multi-service setup
├── init.sql                     # Database initialization
├── tables.json                  # Schema reference (Spider)
├── EVAL_GUIDE.md                # Evaluation guide
└── README.md                    # This file
```

---

## 📊 Evaluation & Testing

### Run Evaluation on ViText2SQL Dataset

The project includes evaluation framework to measure model accuracy:

```bash
# Evaluate on 50 samples
python scripts/eval_vitext2sql.py --split test --limit 50
```

**Output Metrics:**
- **SQL Validity**: % of generated SQL with correct syntax
- **SELECT Only**: % of safe queries (no INSERT/UPDATE/DELETE)
- **Exact Match**: % of exactly matching gold SQL
- **Execution**: % of queries producing correct results

**Results saved to:**
- `backend/eval/outputs/vitext2sql_eval.jsonl` - Per-sample details
- `backend/eval/outputs/vitext2sql_eval_summary.json` - Aggregated metrics

### Analyze Results

```bash
python scripts/analyze_results.py
```

Generates:
- Overall accuracy statistics
- Error patterns and types
- Per-database breakdown
- Sample failures for debugging

### Example Output

```
📊 Evaluation Summary
============================================================
Total Samples: 100
✓ Valid SQL: 68.0%
✓ SELECT Only: 92.0%
✓ Exact Match: 18.0%
❌ Errors: 5 (API quota, parsing, etc.)
============================================================
```

For detailed guide: [EVAL_GUIDE.md](EVAL_GUIDE.md)

---

## 🔧 Configuration

### Environment Variables

Create `.env` in `backend/` folder:

```env
# Required
GEMINI_API_KEY=your_key_here

# Optional (defaults provided)
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/sql_demo
LOG_LEVEL=INFO
```

### Database Connection

Default PostgreSQL setup (in docker-compose.yml):
- **Host**: postgres
- **Port**: 5432
- **User**: postgres
- **Password**: postgres
- **Database**: sql_demo

### Customizing Database

To use different database:

1. Modify `DATABASE_URL` in `.env`
2. Update `init.sql` with your schema
3. Restart: `docker compose down && docker compose up`

---

## 🐛 Troubleshooting

### Issue: "AI Model not available"

**Problem**: Backend starts but returns "AI Model not available" error

**Solutions**:
1. Check Gemini API key is correct
2. Verify API key has permissions
3. Check logs: `docker logs sql-backend`
4. Restart services: `docker compose restart`

```bash
# Debug
docker logs sql-backend
# Look for: "✅ Using Gemini model: models/gemini-2.5-flash"
```

### Issue: Database Connection Error

**Problem**: Backend can't connect to PostgreSQL

**Solutions**:
1. Check PostgreSQL is running: `docker logs sql-postgres`
2. Verify DATABASE_URL is correct
3. Wait 10 seconds for DB to initialize
4. Check logs for specific error

```bash
# Health check
curl http://localhost:8000/api/health
```

### Issue: Quota Exceeded Error

**Problem**: Getting "429 Quota exceeded" from Gemini API

**Causes**:
- Free tier limited to 20 requests/day
- Need to upgrade API plan for higher limits

**Solutions**:
1. Upgrade Gemini API plan (pay-as-you-go)
2. Wait until next day for quota reset
3. Use local model (fine-tuned) instead
4. Reduce evaluation sample limit

```bash
# Evaluate only 10 samples to stay under quota
python scripts/eval_vitext2sql.py --limit 10
```

### Issue: Frontend not loading

**Problem**: http://localhost shows blank page

**Solutions**:
1. Check nginx is running: `docker ps | grep nginx`
2. Try direct file: open `frontend/index.html` in browser
3. Check port 80 is not blocked
4. Restart: `docker compose restart`

---

## 📈 Performance & Optimization

### Response Times

Typical latency breakdown:
- AI SQL Generation: 2-3 seconds (Gemini API)
- Query Execution: 10-100ms (PostgreSQL)
- Total: 2-4 seconds

### Scaling Considerations

For production:
- Add caching layer (Redis) for repeated queries
- Implement query result caching
- Use connection pooling (SQLAlchemy does this)
- Add rate limiting on API

### Cost Estimation

**Gemini API Pricing** (as of 2026):
- Free tier: 20 requests/day
- Standard: $0.075 per 1000 requests
- Batch: Discounted rates for bulk processing

---

## 🎓 Learning Resources

### Understanding the Code

1. **Backend Flow**: [backend/app/main.py](backend/app/main.py)
   - Startup: Load Gemini model
   - Request: Parse question → Generate SQL → Execute

2. **SQL Generation**: [backend/app/ai.py](backend/app/ai.py)
   - Creates prompt with schema context
   - Calls Gemini API
   - Cleans and validates output

3. **Evaluation**: [backend/eval/eval.py](backend/eval/eval.py)
   - Loads ViText2SQL dataset
   - Generates SQL for each question
   - Calculates metrics

### Related Topics

- **Text-to-SQL**: Spider, ViText2SQL, CodeSQL papers
- **LLM Prompting**: Few-shot learning, schema grounding
- **SQL Validation**: sqlparse, AST analysis
- **Database Design**: Normalization, indexing

---

## 🚦 Roadmap

### Current Status
✅ Basic text-to-SQL generation  
✅ PostgreSQL integration  
✅ Evaluation framework  
✅ Docker deployment  

### Planned Features
- [ ] Fine-tune local model (Qwen, CodeLlama)
- [ ] Advanced metrics (TruLens)
- [ ] Query caching & optimization
- [ ] Multi-turn conversation support
- [ ] Natural language result explanation
- [ ] Web-based prompt tuning interface
- [ ] Batch processing API

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

1. **Prompt Engineering**: Better prompts for Vietnamese SQL
2. **Error Handling**: More specific error messages
3. **Performance**: Caching, optimization
4. **Features**: More API endpoints, advanced filtering
5. **Documentation**: More examples, tutorials

### Development Setup

```bash
# Clone and setup
git clone <repo>
cd AI-Text-To-SQL-main
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r backend/requirements.txt

# Run backend locally (no Docker)
cd backend
uvicorn app.main:app --reload --port 8000

# Run tests
python scripts/eval_vitext2sql.py --limit 10
```

---

## 📝 License

MIT License - See LICENSE file for details

---

## 💬 Support & Questions

**Issues & Bugs**: Open GitHub issue with:
- Error message & stack trace
- Steps to reproduce
- Expected vs actual behavior
- Environment (OS, Python version, Docker version)

---

## 📚 References

### Datasets
- [ViText2SQL](https://huggingface.co/datasets/SEACrowd/vitext2sql) - Vietnamese Text-to-SQL
- [Spider](https://yale-lily.github.io/spider) - English Text-to-SQL

### Tools & Libraries
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit
- [Gemini API](https://ai.google.dev/) - LLM provider
- [Docker](https://www.docker.com/) - Containerization

### Papers
- [Spider: A Large-Scale Human-Labeled Dataset for Complex and Cross-Domain Semantic Parsing and Text-to-SQL Task](https://arxiv.org/abs/1809.08887)
- [Text-to-SQL Generation with Schema-Aware Lexicalization and Syntax-Driven Generation](https://arxiv.org/abs/2106.01144)

---

## 🎯 Quick Links

| Link | Purpose |
|------|---------|
| [API Docs](http://localhost:8000/docs) | Interactive API testing |
| [Health Check](http://localhost:8000/api/health) | Service status |
| [Frontend](http://localhost) | Web UI |How to evaluate |
| [Database Logs](docker logs sql-postgres) | Debug DB issues |
| [Backend Logs](docker logs sql-backend) | Debug API issues |

---

**Happy Querying! 🚀**
