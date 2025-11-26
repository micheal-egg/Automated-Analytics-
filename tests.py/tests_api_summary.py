import pytest
from app.api import create_app

@pytest.fixture()

def client():
    
    """
    Create a test client for the Flask application.
    """

    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()

def test_health_endpoint(client):
    """
    Confirm the service is alive and returns expected JSON.
    """
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}

def test_daily_summary_requires_date(client):
    """
    Verify input validation.
    If the user doesn't pass ?date=..., the API should reject it with 400.
    """
    res = client.get("/metrics/daily-summary")
    assert res.status_code == 400

    data = res.get_json()
    assert "error" in data

def test_daily_summary_returns_json_schema(client):
    """
    Verify the API returns the correct schema.
    """
    res = client.get("/metrics/daily-summary?date=2024-11-01")
    assert res.status_code == 200

    data = res.get_json()
    assert set(data.keys()) == {
        "date",
        "total_transactions",
        "total_revenue",
        "avg_rating",
    }

def test_daily_summary_value_ranges(client):
    """
    Verify business rules sanity checks.
    Even if data exists, values should be valid.
    """
    res = client.get("/metrics/daily-summary?date=2024-11-01")
    assert res.status_code == 200

    data = res.get_json()
    assert data["total_transactions"] >= 0
    assert data["total_revenue"] >= 0
    assert 1.0 <= data["avg_rating"] <= 5.0


