# Autonomous Market Intelligence Platform Backend

This is a production-ready, clean-architecture Python FastAPI backend for the Autonomous Market Intelligence Platform.

## Technology Stack

- **Python 3.11**
- **FastAPI**
- **Pydantic v2**
- **Uvicorn** (Dev server)
- **Pytest** & **HTTPX** (Testing)

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── analyze.py
│   │   └── collect.py
│   ├── collectors/
│   │   ├── __init__.py
│   │   ├── ddgs_collector.py
│   │   ├── news_collector.py
│   │   └── competitor_collector.py
│   ├── intelligence/
│   │   ├── __init__.py
│   │   ├── signals.py
│   │   └── opportunities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── evidence.py
│   │   ├── signal.py
│   │   ├── opportunity.py
│   │   ├── threat.py
│   │   ├── market_pulse.py
│   │   └── analysis.py
│   └── services/
│       ├── __init__.py
│       └── analysis_service.py
├── requirements.txt
└── README.md
```

## Running the Application

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the FastAPI server**:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

3. **Access OpenAPI documentation**:
   Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.

## Running Tests

Execute tests from the `backend/` directory:
```bash
python -m pytest
```
