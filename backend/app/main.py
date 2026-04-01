"""
Hawker Centre API

This FastAPI application provides endpoints to retrieve and search
Singapore hawker centre data.

Features:
- List all hawker centres
- Filter by region
- Search by name
- Retrieve a hawker centre by ID

Data is loaded from a local JSON file at startup.
"""

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import json
from pathlib import Path

from .models import (
    HawkerCentre, Region
)

app = FastAPI(title="Hawker Centre API", description="Singapore Hawker Centre Finder")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Loading
DATA_PATH = Path(__file__).parent.parent.parent / "data" / "hawker_centres.json"

def load_hawker_centres() -> List[HawkerCentre]:
    """
    Load hawker centre data from a JSON file and convert it into
    a list of HawkerCentre objects.

    Returns:
        List[HawkerCentre]: A list of hawker centre instances.
    """
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    centres = []
    for item in data:
        centre = HawkerCentre(
            id=item['id'],
            name=item['name'],
            address=item['address'],
            postal_code=item['postal_code'],
            latitude=item['latitude'],
            longitude=item['longitude'],
            region=Region(item['region']),
            total_stalls=item.get('total_stalls', 0),
        )
        centres.append(centre)
    return centres

# Load data into memory
hawker_centres = load_hawker_centres()

# Endpoints
@app.get("/")
async def root():
    """
    Root endpoint of the API.

    Returns:
        dict: Basic API information including total number of hawker centres.
    """
    return {"message": "Hawker Centre API", "total_centres": len(hawker_centres)}

@app.get("/api/hawkers")
async def get_hawkers(
    region: Optional[str] = Query(None, description="Filter by region"),
    search: Optional[str] = Query(None, description="Search by name"),
):
    """
    Retrieve a list of hawker centres with optional filtering.

    Args:
        region (Optional[str]): Filter hawker centres by region.
        search (Optional[str]): Search hawker centres by name (case-insensitive).

    Returns:
        List[dict]: A list of hawker centres matching the filters.

    Raises:
        HTTPException: If the provided region is invalid.
    """
    results = hawker_centres.copy()
    
    if region:
        try:
            region_enum = Region(region)
            results = [h for h in results if h.region == region_enum]
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid region: {region}")
    
    if search:
        results = [h for h in results if search.lower() in h.name.lower()]
    
    return [h.to_dict() for h in results]

@app.get("/api/hawkers/{hawker_id}")
async def get_hawker(hawker_id: int):
    """
    Retrieve a single hawker centre by its ID.

    Args:
        hawker_id (int): The unique identifier of the hawker centre.

    Returns:
        dict: The hawker centre data.

    Raises:
        HTTPException: If the hawker centre is not found.
    """
    for h in hawker_centres:
        if h.id == hawker_id:
            return h.to_dict()
    raise HTTPException(status_code=404, detail="Hawker centre not found")

# Dev Entrypoint
if __name__ == "__main__":
    """
    Run the FastAPI application locally using Uvicorn.

    This is intended for development use only.
    """
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
