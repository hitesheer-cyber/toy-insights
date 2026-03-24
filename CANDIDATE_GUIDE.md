# Candidate Getting Started Guide

## Welcome to Toy Insights!

This is an interview template project that tests your ability to work with:
- **Python backend** (FastAPI, SQLAlchemy)
- **Machine Learning** (embeddings, vector search, RAG)
- **Database design** (PostgreSQL, schema design)
- **Caching** (Redis with TTL)
- **Cloud deployment** (Azure awareness)
- **Testing & debugging** (identifying and fixing bugs)

---

## Step 1: Understand the Project (5 minutes)

### What does this app do?
1. Reads toy product reviews from markdown files
2. Splits them into chunks and creates vector embeddings
3. Stores metadata in a PostgreSQL database
4. Allows users to search via `/search` endpoint or ask questions via `/chat`
5. Uses RAG (Retrieval-Augmented Generation) to answer questions with sources
6. Caches answers in Redis for performance

### Key concepts
- **RAG:** Retrieve relevant documents → Augment prompt with context → Generate answer
- **Embeddings:** Convert text to numerical vectors for similarity search
- **Vector Store:** Index for fast nearest-neighbor search (using FAISS)
- **Caching:** Store recent answers with TTL to avoid redundant work

---

## Step 2: Explore the Code (5 minutes)

### Start here:
1. **[README.md](README.md)** - Project overview
2. **[src/api/main.py](src/api/main.py)** - FastAPI endpoints
3. **[src/api/models.py](src/api/models.py)** - Request/response schemas
4. **[src/rag/pipeline.py](src/rag/pipeline.py)** - RAG orchestration

### Run the tests to understand expected behavior:
```bash
pytest tests/ -v
```

Most tests should pass. Notice that `tests/test_bug.py` **will fail** — that's intentional.

---

## Step 3: Find and Fix the Bug (20 minutes)

### The Challenge
There's a **deliberate bug** in the codebase. Your job is to:
1. Identify the bug by running tests and inspecting code
2. Understand why it causes problems
3. Fix the bug
4. Verify all tests pass

### Finding the Bug
```bash
# Run all tests - one will fail
pytest tests/ -v

# Look specifically at the bug detection test
pytest tests/test_bug.py -v
```

**Hints:**
- The failing test will point you in the right direction
- It's in the ChatRequest class
- Related to a common Python gotcha with default arguments
- Consider how Pydantic handles default values

### Understanding It
Once you find the failing test, read the test code carefully. It demonstrates the problematic behavior. Think about:
- What state is being shared between requests?
- Why would this happen with default values?
- How do mutable vs immutable defaults behave?

### Fixing It
The fix is simple (1-2 lines). Look up Pydantic's `Field` with `default_factory` if you're stuck.

After fixing, verify:
```bash
pytest tests/ -v  # All tests should pass
```

---

## Step 4: Discussion (10 minutes)

Discuss what you've accomplished:

- **The bug:** What was it? How did you identify it?
- **The fix:** What changes did you make? Why were they correct?
- **Testing:** How did you verify the fix worked?
- **Understanding:** Explain key concepts from the codebase

---

## Testing During the Interview

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_bug.py -v
```

---

## FAQ & Troubleshooting

### "I don't have PostgreSQL installed"
No problem! The code falls back to SQLite (see `.env.example`):
```
DATABASE_URL=sqlite:///./toy_insights.db
```

### "Redis not running"
Also fine! The code falls back to in-memory cache (see `src/cache/redis_client.py`).

### "Embedding model download is slow"
First run downloads the model (~100MB). It's cached locally.
Or use mock embeddings (already implemented as fallback).

### "Tests are failing"
1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment: `cp .env.example .env`
3. Initialize DB: `python -c "from src.db.orm import engine; from src.db import schema; schema.init_db(engine)"`
4. Seed data: `python scripts/seed.py`

**Note:** One test is *supposed* to fail initially - that's the bug you need to fix!

### "I broke something"
1. Check git status: `git status`
2. Revert a file: `git checkout src/api/main.py`
3. Reset everything: `git reset --hard`

---

## Time Allocation

- **Understand:** 5 min - Skim docs, run initial tests
- **Explore:** 10 min - Find the failing test, locate bug
- **Fix:** 15 min - Implement fix, verify tests pass
- **Discuss:** 10 min - Explain your work and approach

**Total: 40 minutes**

---

## Key Files to Study

1. **[src/api/main.py](src/api/main.py)** - Start here for API structure
2. **[src/api/models.py](src/api/models.py)** - The bug is here!
3. **[src/rag/pipeline.py](src/rag/pipeline.py)** - RAG orchestration
4. **[tests/test_bug.py](tests/test_bug.py)** - Understanding the bug
5. **[README.md](README.md)** - Full context & evaluation rubric

---

## Quick Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env

# Initialize
python -c "from src.db.orm import engine; from src.db import schema; schema.init_db(engine)"
python scripts/seed.py

# Run
uvicorn src.api.main:app --reload

# Test
pytest tests/ -v
pytest tests/test_bug.py -v  # The failing test

# Docker
docker-compose -f infra/docker/docker-compose.yml up
```

---

## Need Help?

1. **Read the docstrings** — Most functions explain themselves
2. **Look at existing tests** — Show expected behavior
3. **Check error messages** — Usually tell you exactly what's wrong
4. **Ask clarifying questions** — Thoughtful questions demonstrate engagement

---

Good luck! You've got this!
