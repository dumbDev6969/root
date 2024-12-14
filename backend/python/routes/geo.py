import os
import json
from fastapi import APIRouter, HTTPException, Depends
from utils.security import validate_input

router = APIRouter()

base_dir = os.path.dirname(os.path.abspath(__file__))
regions_path = os.path.join(base_dir, '..', 'geo', 'region.json')
provinces_path = os.path.join(base_dir, '..', 'geo', 'province.json')
municipalities_path = os.path.join(base_dir, '..', 'geo', 'municipality.json')

@router.get("/api/regions/{region_code}/provinces/")
async def get_provinces_by_region(region_code: str, _: None = Depends(validate_input)):
    # Validate region code exists
    with open(regions_path, 'r') as f:
        regions = json.load(f)
        if not any(region['code'] == region_code for region in regions):
            raise HTTPException(status_code=404, detail="Region not found")
    
    # Load provinces and filter by region
    with open(provinces_path, 'r') as f:
        provinces = json.load(f)
        
        filtered_provinces = [
            province for province in provinces 
            if province['regionCode'] == region_code
        ]
        
        if not filtered_provinces:
            raise HTTPException(status_code=404, detail="No provinces found for this region")
        
        return filtered_provinces

@router.get("/api/regions")
async def home(_: None = Depends(validate_input)):
    with open(regions_path, 'r') as f:
        regions = json.load(f)  # This correctly parses the JSON file
    return regions

@router.get("/api/provinces/{province_code}/municipalities/")
async def get_municipalities_by_province(province_code: str, _: None = Depends(validate_input)):
    # Validate province code exists
    with open(provinces_path, 'r') as f:
        provinces = json.load(f)
        if not any(province['code'] == province_code for province in provinces):
            raise HTTPException(status_code=404, detail="Province not found")
    
    # Load municipalities and filter by province
    with open(municipalities_path, 'r') as f:
        municipalities = json.load(f)
        
        filtered_municipalities = [
            municipality for municipality in municipalities 
            if municipality['provinceCode'] == province_code
        ]
        
        if not filtered_municipalities:
            raise HTTPException(status_code=404, detail="No municipalities found for this province")
        
        return filtered_municipalities
