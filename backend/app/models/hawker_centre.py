"""
This module defines the core data models for the Hawker Centre API.

- `Region`: An enumeration of Singapore regions used to classify hawker centres.
- `HawkerCentre`: A data model representing a hawker centre.

The `to_dict()` method converts the dataclass into a JSON-serializable dictionary,
which is useful for API responses.
"""

from dataclasses import dataclass
from enum import Enum

class Region(Enum):
    """Enumeration of Singapore regions."""
    NORTH = "North"
    SOUTH = "South"
    EAST = "East"
    WEST = "West"
    CENTRAL = "Central"
    NORTH_EAST = "North-East"

@dataclass
class HawkerCentre:
    """Represents a hawker centre in Singapore."""
    id: int
    name: str
    address: str
    postal_code: str
    latitude: float
    longitude: float
    region: Region
    total_stalls: int = 0
    
    def to_dict(self) -> dict:
        """Convert the HawkerCentre instance into a JSON-serializable dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'postal_code': self.postal_code,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'region': self.region.value,
            'total_stalls': self.total_stalls,
        }
