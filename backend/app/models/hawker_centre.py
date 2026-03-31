from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime

class Region(Enum):
    NORTH = "North"
    SOUTH = "South"
    EAST = "East"
    WEST = "West"
    CENTRAL = "Central"
    NORTH_EAST = "North-East"

@dataclass
class Coordinates:
    latitude: float
    longitude: float
    
    def distance_to(self, other: 'Coordinates') -> float:
        # Calculate distance in km using Haversine formula
        R = 6371
        lat1, lon1 = radians(self.latitude), radians(self.longitude)
        lat2, lon2 = radians(other.latitude), radians(other.longitude)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return R * c

@dataclass
class HawkerCentre:
    id: int
    name: str
    address: str
    postal_code: str
    coordinates: Coordinates
    region: Region
    total_stalls: int = 0
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'postal_code': self.postal_code,
            'latitude': self.coordinates.latitude,
            'longitude': self.coordinates.longitude,
            'region': self.region.value,
            'total_stalls': self.total_stalls,
        }
