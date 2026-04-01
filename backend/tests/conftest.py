"""
Pytest configuration and fixtures for testing the Hawker Centre API.
"""

import pytest
import json
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """
    Create a TestClient for the FastAPI application.
    """
    return TestClient(app)

@pytest.fixture
def sample_hawker_data():
    """
    Provide sample hawker centre data for testing.
    """
    return [
        {
            "id": 1,
            "name": "Maxwell Food Centre",
            "address": "1 Kadayanallur St",
            "postal_code": "069184",
            "latitude": 1.2801,
            "longitude": 103.8451,
            "region": "Central",
            "total_stalls": 100
        },
        {
            "id": 2,
            "name": "Chinatown Complex",
            "address": "335 Smith St",
            "postal_code": "050335",
            "latitude": 1.2838,
            "longitude": 103.8432,
            "region": "Central",
            "total_stalls": 200
        },
        {
            "id": 3,
            "name": "East Coast Lagoon",
            "address": "1220 East Coast Pkwy",
            "postal_code": "468960",
            "latitude": 1.3062,
            "longitude": 103.9264,
            "region": "East",
            "total_stalls": 60
        }
    ]

@pytest.fixture
def temp_data_file(tmp_path, sample_hawker_data):
    """
    Create a temporary JSON file with sample hawker data.
    """
    data_file = tmp_path / "hawker_centres.json"
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(sample_hawker_data, f, indent=2)
    return data_file
