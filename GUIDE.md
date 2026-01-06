# Vietnamese Text-to-SQL Assistant - Complete Guide 📚

A comprehensive guide to understanding, setting up, and using the Text-to-SQL project.

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Quick Start](#quick-start)
4. [Technology Stack](#technology-stack)
5. [API Documentation](#api-documentation)
6. [Configuration](#configuration)
7. [Database Schema](#database-schema)
8. [Testing & Evaluation](#testing--evaluation)
9. [How It Works](#how-it-works)
10. [Security & Best Practices](#security--best-practices)
11. [Troubleshooting](#troubleshooting)
12. [Performance Tips](#performance-tips)

---

## 🎯 Project Overview

**Vietnamese Text-to-SQL** is an AI-powered system that converts natural language Vietnamese questions into SQL queries.

### What It Does
1. **Accepts Vietnamese questions** from users
2. **Analyzes database schema** automatically
3. **Generates SQL queries** using Google Gemini AI
4. **Executes queries** on PostgreSQL
5. **Returns results** as JSON to frontend

### Use Cases
- 📚 Learning AI + Database integration
- 🎓 Teaching SQL and Backend concepts
- 🏢 Building data access layers
- 🚀 Creating internal tools and dashboards
- 🤖 Demonstrating LLM capabilities

---

## 🏗️ Project Structure

```
Text-To-SQL/
├── backend/                      # FastAPI Backend Server
│   ├── app/
│   │   ├── main.py              # FastAPI app initialization & startup
│   │   ├── routes.py            # API endpoint handlers
│   │   ├── ai.py                # Gemini AI integration & prompting
│   │   ├── database.py          # PostgreSQL connection & queries
│   │   ├── schemas.py           # Pydantic request/response models
│   │   ├── config.py            # Configuration & logging setup
│   │   └── utils.py             # Helper functions & SQL validation
│   ├── eval/                    # Evaluation & Testing Framework
│   │   ├── eval.py              # Evaluation pipeline & metrics
│   │   ├── __init__.py
│   │   └── outputs/             # Results & statistics
│   │       ├── vitext2sql_eval.jsonl     # Detailed results
│   │       └── vitext2sql_eval_summary.json  # Summary stats
│   ├── Dockerfile               # Docker image configuration
│   ├── requirements.txt         # Python package dependencies
│   └── .env.example             # Environment template (don't commit .env)
│
├── frontend/                     # Web User Interface
│   ├── index.html               # Main HTML page
│   ├── script.js                # JavaScript logic & API calls
│   └── style.css                # CSS styling & layout
│
├── scripts/                      # Utility Scripts
│   ├── eval_vitext2sql.py       # Evaluation script runner
│   └── analyze_results.py       # Results analysis & visualization
│
├── assets/                       # Images & resources
│   ├── 1.jpg, 2.jpg, 3.jpg, 4.jpg  # Screenshots
│   └── dev.jpeg
│
├── docker-compose.yml           # Multi-container orchestration
├── init.sql                     # Database initialization script
├── tables.json                  # Database schema definition
├── .env.example                 # Global environment template
├── README.md                    # Project overview
├── GUIDE.md                     # This comprehensive guide
└── .gitignore                   # Git ignore rules
```

### Key Directories Explained

**`backend/app/`** - Core application logic
- Single responsibility principle: each file handles one concern
- Modular design for easy testing and maintenance

**`backend/eval/`** - Quality assurance
- Measures AI accuracy
- Tracks SQL validity
- Analyzes error patterns

**`frontend/`** - User-facing interface
- Vanilla JavaScript (no framework overhead)
- RESTful API communication
- Responsive design

**`scripts/`** - Automation & analysis
- Data processing
- Results visualization
- Batch operations

---

## 🚀 Quick Start

### Prerequisites
- **Docker** & **Docker Compose** installed
- **Google Gemini API Key** ([Get it here](https://ai.google.dev/))
- **Git** (optional, for version control)
- **4GB RAM** minimum

### Step-by-Step Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/anhducbui6103/Text-to-sql.git
cd Text-To-SQL
```

#### 2. Setup Environment Variables

**Create root `.env` file:**
```bash
cp .env.example .env
```

Edit `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
BACKEND_URL=http://localhost:8000
```

**Create backend `.env` file:**
```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env`:
```env
DB_URI=postgresql://postgres:postgres123@postgres:5432/textosql_db
GEMINI_API_KEY=your_gemini_api_key_here
```

#### 3. Start Services with Docker
```bash
# Start all services (PostgreSQL, Backend, Frontend)
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend
```

#### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **PostgreSQL**: localhost:5432

#### 5. Verify Setup
```bash
# Check if API is running
curl http://localhost:8000/api/schema

# Should return database schema
```

### Manual Setup (Without Docker)

If you prefer not to use Docker:

```bash
# 1. Install Python dependencies
pip install -r backend/requirements.txt

# 2. Setup PostgreSQL
# Create database and run init.sql
psql -U postgres -d textosql_db < init.sql

# 3. Start backend
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 4. Open frontend
# Simply open frontend/index.html in browser or serve with Python
python -m http.server 3000 --directory frontend
```

---

## 💻 Technology Stack

### Backend

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Framework** | FastAPI | 0.115.0 | Modern async web framework |
| **Server** | Uvicorn | 0.30.6 | ASGI server for async support |
| **Database ORM** | SQLAlchemy | 2.0.35 | Type-safe database queries |
| **DB Driver** | psycopg2-binary | 2.9.9 | PostgreSQL Python adapter |
| **AI Model** | Google Generative AI | 0.8.4 | Gemini API client |
| **Config** | python-dotenv | 1.0.1 | Environment variable management |
| **Data Validation** | Pydantic | Built-in | Request/response models |

### Database
- **PostgreSQL** 16 - ACID-compliant relational database
- **Schema Introspection** - Automatic table/column detection
- **Connection Pooling** - SQLAlchemy handles connection management

### Frontend
- **Vanilla JavaScript** - No framework dependencies (light & fast)
- **HTML5** - Semantic markup
- **CSS3** - Modern styling & responsive design
- **Fetch API** - Async HTTP requests

### DevOps
- **Docker** - Container technology
- **Docker Compose** - Multi-container orchestration
- **Volume Mounting** - Data persistence

### Development Tools
- **Evaluation Framework** - datasets, pandas, tqdm
- **Logging** - Built-in Python logging

---

## 📖 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Response Format
All responses follow a consistent JSON format.

#### Success Response (200)
```json
{
  "success": true,
  "data": {...},
  "message": "Operation successful"
}
```

#### Error Response (400/500)
```json
{
  "success": false,
  "error": "Error message",
  "details": {...}
}
```

---

### API Endpoints

#### 1️⃣ Generate SQL Query

**POST** `/api/generate`

Converts a Vietnamese question into SQL and executes it.

**Request:**
```json
{
  "question": "Danh sách tất cả khách hàng?"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "question": "Danh sách tất cả khách hàng?",
    "generated_sql": "SELECT * FROM customers;",
    "execution_status": "success",
    "results": [
      {"id": 1, "name": "Nguyen Van A", "email": "a@example.com"},
      {"id": 2, "name": "Tran Thi B", "email": "b@example.com"}
    ],
    "row_count": 2,
    "execution_time_ms": 45
  }
}
```

**Error Cases:**
- Invalid question: 400 Bad Request
- API error: 500 Internal Server Error
- SQL execution error: Returns error details in response

---

#### 2️⃣ Get Database Schema

**GET** `/api/schema`

Returns the complete database schema (all tables and columns).

**Response:**
```json
{
  "success": true,
  "data": {
    "tables": [
      {
        "name": "customers",
        "columns": [
          {"name": "id", "type": "integer", "nullable": false},
          {"name": "name", "type": "varchar", "nullable": false},
          {"name": "email", "type": "varchar", "nullable": true},
          {"name": "created_at", "type": "timestamp", "nullable": false}
        ]
      },
      {
        "name": "orders",
        "columns": [
          {"name": "id", "type": "integer", "nullable": false},
          {"name": "customer_id", "type": "integer", "nullable": false},
          {"name": "amount", "type": "decimal", "nullable": false},
          {"name": "status", "type": "varchar", "nullable": true}
        ]
      }
    ]
  }
}
```

---

#### 3️⃣ Execute Custom SQL

**POST** `/api/execute`

Executes custom SQL queries directly (useful for testing).

**Request:**
```json
{
  "sql": "SELECT COUNT(*) as total FROM customers;"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "results": [
      {"total": 42}
    ],
    "row_count": 1,
    "execution_time_ms": 12
  }
}
```

**Security Note:** Validate all SQL before execution in production.

---

#### 4️⃣ Health Check

**GET** `/api/health`

Check if backend is running and connected to database.

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "database": "connected",
    "ai_model": "available"
  }
}
```

---

### Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 400 | Bad Request | Check request format |
| 401 | Unauthorized | Check API key |
| 403 | Forbidden | Check permissions |
| 404 | Not Found | Check endpoint URL |
| 500 | Server Error | Check backend logs |
| 503 | Service Unavailable | Check if services are running |

---

## 🔧 Configuration

### Backend Configuration Files

#### `backend/.env` - Secrets & Keys
```env
# Database Connection
DB_URI=postgresql://postgres:postgres123@postgres:5432/textosql_db

# Gemini AI API
GEMINI_API_KEY=AIzaSy...your_key_here

# Optional: Logging
LOG_LEVEL=INFO

# Optional: Server
API_PORT=8000
API_HOST=0.0.0.0
```

#### `backend/app/config.py` - Application Settings

Reads from environment variables:
```python
DB_URI = os.getenv("DB_URI")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
```

### Environment Variables Reference

| Variable | Type | Required | Example | Description |
|----------|------|----------|---------|-------------|
| `DB_URI` | String | ✅ Yes | `postgresql://...` | Database connection string |
| `GEMINI_API_KEY` | String | ✅ Yes | `AIzaSy...` | Google Gemini API key |
| `LOG_LEVEL` | String | ❌ No | `INFO` | Logging verbosity |
| `API_PORT` | Integer | ❌ No | `8000` | Backend server port |
| `BACKEND_URL` | String | ❌ No | `http://localhost:8000` | Backend URL for frontend |

### Getting Your Gemini API Key

1. Go to [Google AI Studio](https://ai.google.dev/)
2. Click "Get API Key"
3. Create new API key
4. Copy and paste into `.env` file

---

## 📊 Database Schema

### Schema Definition (`tables.json`)

```json
{
  "customers": {
    "columns": {
      "id": "SERIAL PRIMARY KEY",
      "name": "VARCHAR(100) NOT NULL",
      "email": "VARCHAR(100)",
      "phone": "VARCHAR(20)",
      "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    }
  },
  "orders": {
    "columns": {
      "id": "SERIAL PRIMARY KEY",
      "customer_id": "INTEGER NOT NULL REFERENCES customers(id)",
      "amount": "DECIMAL(10, 2) NOT NULL",
      "status": "VARCHAR(50) DEFAULT 'pending'",
      "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    }
  }
}
```

### Database Initialization (`init.sql`)

Run during startup:
```bash
psql -U postgres -d textosql_db < init.sql
```

### Schema Introspection

The `database.py` automatically detects:
- All tables in the database
- All columns and their types
- Primary & foreign key relationships
- Data types and constraints

This schema is sent to Gemini for context.

---

## 🧪 Testing & Evaluation

### Purpose
Measure how well the AI generates SQL queries in different scenarios.

### Running Evaluation

```bash
cd backend

# Run full evaluation
python -m eval.eval

# Or with custom settings
python -m eval.eval --batch_size=10 --test_samples=100
```

### What Gets Measured

1. **SQL Validity** ✓
   - Is the SQL syntactically correct?
   - Can PostgreSQL parse it?

2. **Exact Match** ✓
   - Does generated SQL exactly match expected?
   - Useful for benchmark comparison

3. **Execution Success** ✓
   - Does the query run without errors?
   - No permissions or syntax issues?

4. **Result Accuracy** ✓
   - Are the returned results correct?
   - Matches expected output?

### Results Format

**Detailed Results** (`vitext2sql_eval.jsonl`)
```json
{
  "id": 1,
  "question": "Danh sách khách hàng?",
  "expected_sql": "SELECT * FROM customers;",
  "generated_sql": "SELECT * FROM customers;",
  "exact_match": true,
  "execution_success": true,
  "result_accurate": true,
  "execution_time_ms": 45
}
```

**Summary** (`vitext2sql_eval_summary.json`)
```json
{
  "total_questions": 100,
  "exact_match_rate": 0.85,
  "execution_success_rate": 0.92,
  "result_accuracy_rate": 0.88,
  "average_execution_time_ms": 52.3
}
```

### Analyze Results

```bash
python ../scripts/analyze_results.py
```

Output:
- Success/failure breakdown
- Error pattern analysis
- Performance metrics
- Visualizations (if matplotlib installed)

---

## 🔄 How It Works

### Complete Request-Response Flow

```
User Question (Vietnamese)
       ↓
┌─────────────────────────────────┐
│    Frontend (index.html)        │
│  - Send question to backend     │
└─────────────────────────────────┘
       ↓
┌─────────────────────────────────┐
│  FastAPI Backend (main.py)      │
│  - Receive request              │
│  - Validate input               │
└─────────────────────────────────┘
       ↓
┌─────────────────────────────────┐
│ Database (database.py)          │
│ - Connect to PostgreSQL         │
│ - Introspect schema             │
│ - Get table structure           │
└─────────────────────────────────┘
       ↓
┌─────────────────────────────────┐
│ AI Module (ai.py)               │
│ - Prepare prompt with schema    │
│ - Send to Gemini API            │
│ - Receive SQL query             │
│ - Parse response                │
└─────────────────────────────────┘
       ↓
┌─────────────────────────────────┐
│ Validation (utils.py)           │
│ - Check SQL syntax              │
│ - Validate against schema       │
│ - Security checks               │
└─────────────────────────────────┘
       ↓
┌─────────────────────────────────┐
│ Execution (database.py)         │
│ - Execute SQL on PostgreSQL     │
│ - Get results                   │
│ - Handle errors                 │
└─────────────────────────────────┘
       ↓
┌─────────────────────────────────┐
│ Response (routes.py)            │
│ - Format results as JSON        │
│ - Include metadata              │
│ - Send to frontend              │
└─────────────────────────────────┘
       ↓
Result Displayed to User
```

### Key Components Deep Dive

#### 1. **routes.py** - API Endpoints
Handles HTTP requests:
```python
@router.post("/generate")
async def generate_sql(request: GenerateRequest):
    # Extract question from request
    # Call AI module
    # Execute SQL
    # Return results
```

#### 2. **ai.py** - Gemini Integration
Sends context to AI:
```python
async def generate_sql_with_gemini(question, schema):
    prompt = f"""
    Database schema:
    {schema}
    
    User question: {question}
    
    Generate SQL query...
    """
    response = await gemini_client.generate(prompt)
    return response
```

#### 3. **database.py** - PostgreSQL Interface
Database operations:
```python
async def get_schema():
    # SELECT table_name, column_name, data_type FROM ...
    return schema_dict

async def execute_query(sql):
    # Validate SQL
    # Execute on PostgreSQL
    # Return results
```

#### 4. **utils.py** - Helper Functions
Validation & formatting:
```python
def validate_sql(sql):
    # Check syntax
    # Prevent SQL injection
    # Return validity status

def format_results(rows):
    # Convert to JSON serializable format
    # Add metadata
    return formatted_results
```

---

## ⚠️ Security & Best Practices

### Critical Security Rules

1. **Never commit `.env` files**
   - Already in `.gitignore`
   - Contains API keys & passwords
   - Use `.env.example` as template

2. **SQL Injection Prevention**
   - Always use parameterized queries (SQLAlchemy ORM)
   - Validate & sanitize SQL before execution
   - Never concatenate user input directly

3. **API Key Management**
   - Store in environment variables only
   - Rotate keys regularly
   - Use separate keys per environment (dev/staging/prod)
   - Never share or commit keys

4. **Database Security**
   - Use strong passwords
   - Limit database user permissions
   - Enable SSL for remote connections
   - Regular backups

5. **Rate Limiting**
   - Implement in production
   - Prevent API abuse
   - Protect against DoS attacks

6. **Authentication**
   - Add in production (JWT tokens)
   - Validate all requests
   - Log access attempts

### Implementation Checklist

- [ ] Use environment variables for all secrets
- [ ] Implement input validation
- [ ] Add authentication layer
- [ ] Enable CORS only for trusted domains
- [ ] Log all database queries
- [ ] Regular security audits
- [ ] Keep dependencies updated
- [ ] Use HTTPS in production

---

## 🐛 Troubleshooting

### Problem: "GEMINI_API_KEY is missing"

**Symptoms:**
```
❌ GEMINI_API_KEY is missing
Application startup failed
```

**Solutions:**
```bash
# 1. Check if .env exists
ls -la backend/.env

# 2. Verify key is set
cat backend/.env | grep GEMINI_API_KEY

# 3. Set manually (temporary)
export GEMINI_API_KEY=your_key_here

# 4. Restart backend
docker-compose restart backend
```

---

### Problem: "Connection refused" to PostgreSQL

**Symptoms:**
```
psycopg2.OperationalError: could not connect to server
```

**Solutions:**
```bash
# 1. Check if PostgreSQL is running
docker-compose ps

# 2. View PostgreSQL logs
docker-compose logs postgres

# 3. Restart PostgreSQL
docker-compose restart postgres

# 4. Check database URI format
echo $DB_URI

# 5. Verify credentials
# Default: postgresql://postgres:postgres123@postgres:5432/textosql_db
```

---

### Problem: "No module named 'fastapi'"

**Symptoms:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solutions:**
```bash
# 1. Install dependencies
pip install -r backend/requirements.txt

# 2. Check Python version (need 3.9+)
python --version

# 3. Rebuild Docker image
docker-compose build --no-cache backend

# 4. Verify virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

---

### Problem: Database schema not detected

**Symptoms:**
```
Schema tables: []
No tables found in database
```

**Solutions:**
```bash
# 1. Reinitialize database
docker-compose exec postgres psql -U postgres -d textosql_db < init.sql

# 2. Verify tables exist
docker-compose exec postgres psql -U postgres -d textosql_db -c "\dt"

# 3. Check connection
curl http://localhost:8000/api/schema

# 4. View backend logs
docker-compose logs backend
```

---

### Problem: Frontend can't reach backend

**Symptoms:**
```
CORS error: Access-Control-Allow-Origin
Failed to fetch from API
```

**Solutions:**
```bash
# 1. Check backend is running
curl http://localhost:8000/api/health

# 2. Check CORS configuration (main.py)
# Verify allow_origins includes frontend URL

# 3. Check API base URL in frontend/script.js
// Should be: http://localhost:8000/api

# 4. Check browser console for exact error
# F12 → Console tab
```

---

### Problem: Slow query execution

**Symptoms:**
```
Execution time: 2000ms+ (very slow)
Frontend timeout errors
```

**Solutions:**
```bash
# 1. Check database indexes
SELECT * FROM pg_indexes WHERE tablename='customers';

# 2. Analyze query plan
EXPLAIN ANALYZE SELECT ...

# 3. Check database load
docker stats postgres

# 4. Monitor backend performance
# Check backend logs for query times

# 5. Enable connection pooling
# SQLAlchemy already does this
```

---

## 📈 Performance Tips

### 1. Database Optimization
- Add indexes to frequently queried columns
- Use `EXPLAIN ANALYZE` to understand query plans
- Denormalize if necessary for read-heavy workloads
- Regular VACUUM and ANALYZE commands

```sql
-- Add index on frequently queried column
CREATE INDEX idx_customers_email ON customers(email);

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM customers WHERE email = 'test@example.com';
```

### 2. API Optimization
- Implement pagination for large result sets
- Cache schema (doesn't change often)
- Use connection pooling (SQLAlchemy default)
- Compress responses (gzip)

```python
# Add to main.py for compression
from fastapi.middleware.gzip import GZIPMiddleware
app.add_middleware(GZIPMiddleware, minimum_size=1000)
```

### 3. AI Model Optimization
- Use caching for schema-related prompts
- Batch process multiple questions
- Use faster models for simple queries
- Implement timeout for API calls

### 4. Frontend Optimization
- Lazy load results
- Debounce search input
- Cache results locally
- Use WebWorkers for heavy processing

### 5. Infrastructure Optimization
- Vertical scaling: More CPU/RAM
- Horizontal scaling: Load balancer + multiple backends
- Database replication for read scaling
- CDN for static assets

### 6. Monitoring
```bash
# Check resource usage
docker stats

# View logs in real-time
docker-compose logs -f

# Check database connections
SELECT count(*) FROM pg_stat_activity;
```

---

## 📝 Common Commands

### Docker Commands
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f backend

# Access container shell
docker-compose exec backend bash

# Rebuild image
docker-compose build --no-cache
```

### Database Commands
```bash
# Access PostgreSQL
docker-compose exec postgres psql -U postgres -d textosql_db

# Useful PostgreSQL commands
\dt              # List tables
\d table_name    # Describe table
\q               # Quit
```

### Python Commands
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Run evaluation
python -m eval.eval

# Analyze results
python ../scripts/analyze_results.py
```

---

## 🤝 Getting Help

1. **Check logs first**
   ```bash
   docker-compose logs backend
   ```

2. **Review API documentation**
   - Swagger UI: http://localhost:8000/docs

3. **Check GitHub Issues**
   - https://github.com/anhducbui6103/Text-to-sql/issues

4. **Read source code**
   - Well-commented for learning

5. **Run evaluation**
   - Helps understand system behavior

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Google Gemini API](https://ai.google.dev/)
- [Docker Documentation](https://docs.docker.com/)

---

**Last Updated**: January 2026
**Version**: 1.0.0
**Author**: Anh Duc Bui
