from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import json
from pathlib import Path
from datetime import datetime

from .models import (
    HawkerCentre, Coordinates, Region
)

app = FastAPI(title="Hawker Centre API", description="Singapore Hawker Centre Finder")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data
DATA_PATH = Path(__file__).parent.parent.parent / "data" / "hawker_centres.json"

def load_hawker_centres() -> List[HawkerCentre]:
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    centres = []
    for item in data:
        centre = HawkerCentre(
            id=item['id'],
            name=item['name'],
            address=item['address'],
            postal_code=item['postal_code'],
            coordinates=Coordinates(item['latitude'], item['longitude']),
            region=Region(item['region']),
            total_stalls=item.get('total_stalls', 0),
        )
        centres.append(centre)
    return centres

hawker_centres = load_hawker_centres()

# Endpoints
@app.get("/")
async def root():
    return {"message": "Hawker Centre API", "total_centres": len(hawker_centres)}

@app.get("/api/hawkers")
async def get_hawkers(
    region: Optional[str] = Query(None, description="Filter by region"),
    search: Optional[str] = Query(None, description="Search by name"),
):
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
    for h in hawker_centres:
        if h.id == hawker_id:
            return h.to_dict()
    raise HTTPException(status_code=404, detail="Hawker centre not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
