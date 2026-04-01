"""
Tests for the FastAPI endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

class TestRootEndpoint:
    """Tests for the root endpoint (/)"""

    def test_root_returns_correct_data(self, client: TestClient):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "Hawker Centre API"
        assert "total_centres" in data
        assert isinstance(data["total_centres"], int)
        assert data["total_centres"] > 0


class TestGetHawkers:
    """Tests for /api/hawkers endpoint"""

    def test_get_all_hawkers(self, client: TestClient):
        response = client.get("/api/hawkers")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        first = data[0]
        for key in ["id", "name", "address", "postal_code", "latitude", "longitude", "region", "total_stalls"]:
            assert key in first

    def test_filter_by_region_central(self, client: TestClient):
        response = client.get("/api/hawkers?region=Central")
        assert response.status_code == 200
        data = response.json()
        for hawker in data:
            assert hawker["region"] == "Central"

    def test_filter_by_region_east(self, client: TestClient):
        response = client.get("/api/hawkers?region=East")
        assert response.status_code == 200
        data = response.json()
        for hawker in data:
            assert hawker["region"] == "East"

    def test_filter_by_search(self, client: TestClient):
        response = client.get("/api/hawkers?search=Maxwell")
        assert response.status_code == 200
        data = response.json()
        for hawker in data:
            assert "maxwell" in hawker["name"].lower()

    def test_filter_by_search_case_insensitive(self, client: TestClient):
        response = client.get("/api/hawkers?search=MAXWELL")
        assert response.status_code == 200
        data = response.json()
        for hawker in data:
            assert "maxwell" in hawker["name"].lower()

    def test_filter_with_no_results(self, client: TestClient):
        response = client.get("/api/hawkers?search=NonExistentName12345")
        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_filter_by_invalid_region(self, client: TestClient):
        response = client.get("/api/hawkers?region=InvalidRegion")
        assert response.status_code == 400
        data = response.json()
        assert "Invalid region" in data["detail"]

    def test_filter_by_region_and_search(self, client: TestClient):
        response = client.get("/api/hawkers?region=Central&search=Maxwell")
        assert response.status_code == 200
        data = response.json()
        for hawker in data:
            assert hawker["region"] == "Central"
            assert "maxwell" in hawker["name"].lower()
