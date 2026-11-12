import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from fastapi.testclient import TestClient  # noqa: E402

from pricecompare.app import app  # noqa: E402

client = TestClient(app)


def test_api_search():
    response = client.get("/api/search", params={"q": "coffee"})
    assert response.status_code == 200
    data = response.json()
    assert data["best"]["shop"] == "BudgetBazaar"


def test_api_search_needs_query():
    assert client.get("/api/search").status_code == 422


def test_home_page_shows_results():
    response = client.get("/", params={"q": "shoes"})
    assert response.status_code == 200
    assert "Best choice" in response.text


def test_home_page_escapes_input():
    response = client.get("/", params={"q": "<script>"})
    assert "<script>" not in response.text