"""
Tests for the data models (HawkerCentre and Region).
"""

import pytest
from app.models import HawkerCentre, Region

class TestRegion:
    """Test cases for the Region enum."""
    
    def test_region_values(self):
        """Test that each region has the correct string value."""
        assert Region.NORTH.value == "North"
        assert Region.SOUTH.value == "South"
        assert Region.EAST.value == "East"
        assert Region.WEST.value == "West"
        assert Region.CENTRAL.value == "Central"
        assert Region.NORTH_EAST.value == "North-East"
    
    def test_region_from_string(self):
        """Test creating a Region from a string."""
        assert Region("Central") == Region.CENTRAL
        assert Region("North") == Region.NORTH
    
    def test_invalid_region_raises_error(self):
        """Test that an invalid region string raises ValueError."""
        with pytest.raises(ValueError):
            Region("InvalidRegion")

class TestHawkerCentre:
    """Test cases for the HawkerCentre dataclass."""
    
    def test_create_hawker_centre(self):
        """Test creating a HawkerCentre instance."""
        centre = HawkerCentre(
            id=1,
            name="Maxwell Food Centre",
            address="1 Kadayanallur St",
            postal_code="069184",
            latitude=1.2801,
            longitude=103.8451,
            region=Region.CENTRAL,
            total_stalls=100
        )
        
        assert centre.id == 1
        assert centre.name == "Maxwell Food Centre"
        assert centre.address == "1 Kadayanallur St"
        assert centre.postal_code == "069184"
        assert centre.latitude == 1.2801
        assert centre.longitude == 103.8451
        assert centre.region == Region.CENTRAL
        assert centre.total_stalls == 100
    
    def test_create_hawker_centre_with_default_stalls(self):
        """Test creating a HawkerCentre without total_stalls (should default to 0)."""
        centre = HawkerCentre(
            id=2,
            name="Test Centre",
            address="Test Address",
            postal_code="123456",
            latitude=1.2801,
            longitude=103.8451,
            region=Region.CENTRAL
        )
        
        assert centre.total_stalls == 0
    
    def test_to_dict(self):
        """Test converting a HawkerCentre to a dictionary."""
        centre = HawkerCentre(
            id=1,
            name="Maxwell Food Centre",
            address="1 Kadayanallur St",
            postal_code="069184",
            latitude=1.2801,
            longitude=103.8451,
            region=Region.CENTRAL,
            total_stalls=100
        )
        
        result = centre.to_dict()
        
        assert isinstance(result, dict)
        assert result['id'] == 1
        assert result['name'] == "Maxwell Food Centre"
        assert result['address'] == "1 Kadayanallur St"
        assert result['postal_code'] == "069184"
        assert result['latitude'] == 1.2801
        assert result['longitude'] == 103.8451
        assert result['region'] == "Central"
        assert result['total_stalls'] == 100
        assert len(result) == 8  # All fields present
    
    def test_to_dict_contains_all_fields(self):
        """Test that to_dict includes all expected fields."""
        centre = HawkerCentre(
            id=1,
            name="Test",
            address="Test Address",
            postal_code="123456",
            latitude=1.0,
            longitude=103.0,
            region=Region.NORTH
        )
        
        result = centre.to_dict()
        expected_keys = {'id', 'name', 'address', 'postal_code', 
                        'latitude', 'longitude', 'region', 'total_stalls'}
        
        assert set(result.keys()) == expected_keys