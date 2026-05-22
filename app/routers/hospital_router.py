from fastapi import APIRouter, Query
from typing import Optional
from app.ai_core.hospital_finder import hospital_finder
from app.ai_core.hospital_finder import hospital_finder


router = APIRouter()

@router.get("/hospitals")
def search_hospitals(
    location: Optional[str] = Query(None, description="City or address"),
    latitude: Optional[float] = Query(None),
    longitude: Optional[float] = Query(None),
    specialty: Optional[str] = Query(None),
    urgency: str = Query("routine"),
    max_distance_km: float = Query(50.0),
    max_results: int = Query(10)
):
    """
    Smart hospital search endpoint
    """
    result = hospital_finder.search_hospitals(
        location=location,
        latitude=latitude,
        longitude=longitude,
        specialty=specialty,
        urgency=urgency,
        max_distance_km=max_distance_km,
        max_results=max_results
    )

    return result


@router.get("/hospitals/{hospital_id}")
def get_hospital_details(hospital_id: str):
    """
    Get detailed hospital info
    """
    hospital = hospital_finder.get_hospital_by_id(hospital_id)
    if not hospital:
        return {"success": False, "error": "Hospital not found"}
    return {"success": True, "hospital": hospital}


@router.get("/hospital-specialties")
def get_specialties():
    """
    Get available medical specialties
    """
    return {
        "success": True,
        "specialties": hospital_finder.get_specialties_list()
    }
