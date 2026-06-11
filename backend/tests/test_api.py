import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health check route."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "version" in response.json()

def test_collect_endpoint():
    """Test POST /collect with valid request."""
    payload = {
        "query": "Competitor Y features",
        "sources": ["ddgs", "news"]
    }
    response = client.post("/collect", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    
    # Verify model structure in response
    first_item = data[0]
    assert "id" in first_item
    assert "source" in first_item
    assert "content" in first_item
    assert "confidence" in first_item
    assert "timestamp" in first_item
    assert "metadata" in first_item

def test_collect_endpoint_invalid_source():
    """Test POST /collect with missing sources."""
    payload = {
        "query": "Competitor Y features",
        "sources": []
    }
    response = client.post("/collect", json=payload)
    # At least one source must be provided
    assert response.status_code == 400

def test_analyze_endpoint():
    """Test POST /analyze and verify downstream effects on market pulse and opportunities."""
    payload = {
        "topic": "SaaS Billing Competitor",
        "focus_areas": ["pricing", "features"],
        "collectors": ["ddgs", "competitor"]
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert "request_id" in data
    assert data["status"] == "completed"
    assert "signals_found" in data
    assert "opportunities_found" in data
    assert "threats_found" in data
    assert "pulse" in data

    # Verify that in-memory state got populated
    # 1. Test GET /opportunities
    opps_response = client.get("/opportunities")
    assert opps_response.status_code == 200
    opps = opps_response.json()
    assert isinstance(opps, list)
    assert len(opps) > 0
    assert opps[0]["value_score"] >= 0.0

    # 2. Test GET /market-pulse
    pulse_response = client.get("/market-pulse")
    assert pulse_response.status_code == 200
    pulse = pulse_response.json()
    assert "market_sentiment" in pulse
    assert pulse["active_signals_count"] > 0
    assert len(pulse["top_opportunities"]) > 0
    assert "metadata" in pulse
