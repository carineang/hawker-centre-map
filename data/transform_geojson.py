"""
GeoJSON to JSON Transformer for Singapore Hawker Centres

This script processes a GeoJSON file containing hawker centre data and
converts it into a clean, structured JSON format suitable for APIs.

Features:
- Extracts relevant properties (name, address, coordinates, etc.)
- Infers region based on postal code
- Cleans and formats address fields
- Outputs a simplified JSON dataset

Usage:
    python script.py
"""

import json

def assign_region(postal_code):
    """
    Determine the Singapore region based on the postal code prefix.

    Args:
        postal_code (str): The postal code of the location.

    Returns:
        str: The region name (e.g., 'Central', 'East'), or 'Unknown'
             if the postal code is invalid or not mapped.
    """
    if not postal_code or len(str(postal_code)) < 2:
        return 'Unknown'
    
    try:
        first_two = int(str(postal_code)[:2])
    except ValueError:
        return 'Unknown'

    # Region mapping based on postal code ranges
    central = {1,2,3,4,5,6,7,8,9,10,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41}
    east = {42,43,44,45,46,47,48,49,50,51,52,81}
    north_east = {53,54,55,56,57,79,80,82}
    west = {11,12,13,58,59,60,61,62,63,64,65,66,67,68,69,70,71}
    north = {72,73,75,76,77,78}

    if first_two in central:
        return 'Central'
    elif first_two in east:
        return 'East'
    elif first_two in north_east:
        return 'North-East'
    elif first_two in west:
        return 'West'
    elif first_two in north:
        return 'North'
    else:
        return 'Unknown'

def transform_geojson_to_clean_json():
    """
    Transform the default GeoJSON file ('hawker.geojson') into a cleaned JSON file
    ('hawker_centres.json').

    Returns:
        List[Dict[str, Any]]: A list of cleaned hawker centre records.
    """
    # Load GeoJSON file
    with open('hawker.geojson', 'r', encoding='utf-8') as f:
        geojson = json.load(f)

    cleaned_centres = []

    for feature in geojson.get('features', []):
        props = feature.get('properties', {})
        coords = feature.get('geometry', {}).get('coordinates', [None, None])

        # Skip invalid entries
        if not props.get('NAME') or coords[0] is None or coords[1] is None:
            continue

        # Build full address
        full_address = props.get('ADDRESS_MYENV')
        if not full_address:
            block = props.get('ADDRESSBLOCKHOUSENUMBER', '')
            street = props.get('ADDRESSSTREETNAME', '')
            postal = props.get('ADDRESSPOSTALCODE', '')
            full_address = f"{block} {street}, Singapore {postal}".strip()

        postal_code = props.get('ADDRESSPOSTALCODE', '')
        region = assign_region(postal_code)

        # Cleaned record
        cleaned = {
            'id': props.get('OBJECTID', len(cleaned_centres) + 1),
            'name': props.get('NAME', '').title(),
            'address': full_address,
            'postal_code': postal_code,
            'region': region,
            'latitude': float(coords[1]),
            'longitude': float(coords[0]),
            'total_stalls': props.get('NUMBER_OF_COOKED_FOOD_STALLS', 0)
        }

        cleaned_centres.append(cleaned)

    # Save to JSON
    with open('hawker_centres.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_centres, f, indent=2, ensure_ascii=False)

    print(f"Processed {len(cleaned_centres)} hawker centres")
    return cleaned_centres

if __name__ == "__main__":
    """
    Execute the transformation script when run directly.
    """
    transform_geojson_to_clean_json()
