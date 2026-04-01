"""
Tests for data loading and validation.
"""

import pytest
import json
from pathlib import Path
from app.main import load_hawker_centres
from app.models import Region

class TestDataLoading:
    """Test data loading functionality."""
    
    def test_data_file_exists(self):
        """Test that the data file exists."""
        data_path = Path(__file__).parent.parent.parent / "data" / "hawker_centres.json"
        assert data_path.exists(), f"Data file not found at {data_path}"
    
    def test_data_file_is_valid_json(self):
        """Test that the data file contains valid JSON."""
        data_path = Path(__file__).parent.parent.parent / "data" / "hawker_centres.json"
        
        with open(data_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                assert isinstance(data, list)
                assert len(data) > 0
            except json.JSONDecodeError:
                pytest.fail("Data file is not valid JSON")
    
    def test_load_hawker_centres_returns_list(self):
        """Test that load_hawker_centres returns a list."""
        centres = load_hawker_centres()
        assert isinstance(centres, list)
        assert len(centres) > 0
    
    def test_load_hawker_centres_returns_correct_type(self):
        """Test that load_hawker_centres returns HawkerCentre objects."""
        from app.models import HawkerCentre
        centres = load_hawker_centres()
        
        assert isinstance(centres[0], HawkerCentre)
    
    def test_each_hawker_has_required_fields(self):
        """Test that each hawker has all required fields."""
        data_path = Path(__file__).parent.parent.parent / "data" / "hawker_centres.json"
        
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        required_fields = ['id', 'name', 'address', 'postal_code', 
                          'latitude', 'longitude', 'region']
        
        for hawker in data:
            for field in required_fields:
                assert field in hawker, \
                    f"Missing field '{field}' in hawker {hawker.get('id', 'unknown')}"
    
    def test_coordinates_are_valid_singapore(self):
        """Test that coordinates are within Singapore bounds."""
        data_path = Path(__file__).parent.parent.parent / "data" / "hawker_centres.json"
        
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Singapore coordinates bounds
        MIN_LAT, MAX_LAT = 1.2, 1.5
        MIN_LNG, MAX_LNG = 103.6, 104.1
        
        for hawker in data:
            lat = hawker['latitude']
            lng = hawker['longitude']
            
            assert MIN_LAT <= lat <= MAX_LAT, \
                f"Invalid latitude {lat} for {hawker['name']}"
            assert MIN_LNG <= lng <= MAX_LNG, \
                f"Invalid longitude {lng} for {hawker['name']}"
    
    def test_region_values_are_valid(self):
        """Test that all region values are valid enum values."""
        data_path = Path(__file__).parent.parent.parent / "data" / "hawker_centres.json"
        
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        valid_regions = [r.value for r in Region]
        
        for hawker in data:
            region = hawker['region']
            assert region in valid_regions, \
                f"Invalid region '{region}' for {hawker['name']}"
    
    def test_total_stalls_is_non_negative(self):
        """Test that total_stalls is a non-negative integer."""
        data_path = Path(__file__).parent.parent.parent / "data" / "hawker_centres.json"
        
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for hawker in data:
            stalls = hawker.get('total_stalls', 0)
            assert isinstance(stalls, int)
            assert stalls >= 0, f"Negative stalls for {hawker['name']}"
            