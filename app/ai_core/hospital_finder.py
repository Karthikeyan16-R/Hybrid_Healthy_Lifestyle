# app/ai_core/hospital_finder.py
import os
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from math import radians, cos, sin, asin, sqrt
import requests

@dataclass
class Hospital:
    """Hospital data model"""
    id: str
    name: str
    address: str
    city: str
    state: str
    pincode: str
    latitude: float
    longitude: float
    phone: str
    specialties: List[str]
    rating: float
    total_reviews: int
    emergency_services: bool
    has_icu: bool
    has_ambulance: bool
    is_24x7: bool
    distance_km: Optional[float] = None
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "pincode": self.pincode,
            "phone": self.phone,
            "specialties": self.specialties,
            "rating": self.rating,
            "total_reviews": self.total_reviews,
            "emergency_services": self.emergency_services,
            "has_icu": self.has_icu,
            "has_ambulance": self.has_ambulance,
            "is_24x7": self.is_24x7,
            "distance_km": round(self.distance_km, 2) if self.distance_km else None,
            "google_maps_url": self._generate_maps_url()
        }
    
    def _generate_maps_url(self) -> str:
        """Generate Google Maps link"""
        return f"https://www.google.com/maps/search/?api=1&query={self.latitude},{self.longitude}"


class SmartHospitalFinder:
    """
    Intelligent hospital finder with location-based search,
    specialty filtering, and emergency routing
    """
    
    # Medical specialties
    SPECIALTIES = {
        "general": "General Medicine",
        "cardiology": "Cardiology (Heart)",
        "neurology": "Neurology (Brain & Nervous System)",
        "orthopedics": "Orthopedics (Bones & Joints)",
        "pediatrics": "Pediatrics (Children)",
        "gynecology": "Gynecology (Women's Health)",
        "oncology": "Oncology (Cancer)",
        "dermatology": "Dermatology (Skin)",
        "ophthalmology": "Ophthalmology (Eye)",
        "ent": "ENT (Ear, Nose, Throat)",
        "gastroenterology": "Gastroenterology (Digestive System)",
        "urology": "Urology (Urinary System)",
        "psychiatry": "Psychiatry (Mental Health)",
        "emergency": "Emergency Medicine",
        "surgery": "General Surgery"
    }
    
    def __init__(self, database_path: Optional[str] = None):
        """
        Initialize hospital finder
        
        Args:
            database_path: Path to hospital database JSON file
        """
        self.hospitals: List[Hospital] = []
        
        # Load hospital database
        if database_path and os.path.exists(database_path):
            self._load_database(database_path)
        else:
            # Use sample database for demonstration
            self._load_sample_database()
    
    def _load_database(self, path: str):
        """Load hospitals from JSON database"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    self.hospitals.append(Hospital(**item))
            print(f"✅ Loaded {len(self.hospitals)} hospitals from database")
        except Exception as e:
            print(f"❌ Error loading database: {e}")
            self._load_sample_database()
    
    def _load_sample_database(self):
        """Load sample hospital data for testing"""
        sample_hospitals = [
            {
                "id": "H001",
                "name": "Apollo Hospital",
                "address": "21, Greams Lane, Off Greams Road",
                "city": "Chennai",
                "state": "Tamil Nadu",
                "pincode": "600006",
                "latitude": 13.0569,
                "longitude": 80.2425,
                "phone": "+91-44-2829-3333",
                "specialties": ["cardiology", "neurology", "oncology", "orthopedics", "emergency"],
                "rating": 4.5,
                "total_reviews": 1250,
                "emergency_services": True,
                "has_icu": True,
                "has_ambulance": True,
                "is_24x7": True
            },
            {
                "id": "H002",
                "name": "Fortis Hospital",
                "address": "154/9, Bannerghatta Road",
                "city": "Bangalore",
                "state": "Karnataka",
                "pincode": "560076",
                "latitude": 12.8698,
                "longitude": 77.6036,
                "phone": "+91-80-6621-4444",
                "specialties": ["cardiology", "orthopedics", "gastroenterology", "urology"],
                "rating": 4.3,
                "total_reviews": 980,
                "emergency_services": True,
                "has_icu": True,
                "has_ambulance": True,
                "is_24x7": True
            },
            {
                "id": "H003",
                "name": "AIIMS Delhi",
                "address": "Ansari Nagar",
                "city": "New Delhi",
                "state": "Delhi",
                "pincode": "110029",
                "latitude": 28.5672,
                "longitude": 77.2100,
                "phone": "+91-11-2658-8500",
                "specialties": ["general", "cardiology", "neurology", "pediatrics", "surgery", "emergency"],
                "rating": 4.6,
                "total_reviews": 2100,
                "emergency_services": True,
                "has_icu": True,
                "has_ambulance": True,
                "is_24x7": True
            },
            {
                "id": "H004",
                "name": "Lilavati Hospital",
                "address": "A-791, Bandra Reclamation",
                "city": "Mumbai",
                "state": "Maharashtra",
                "pincode": "400050",
                "latitude": 19.0544,
                "longitude": 72.8239,
                "phone": "+91-22-2640-5000",
                "specialties": ["cardiology", "orthopedics", "gynecology", "pediatrics"],
                "rating": 4.4,
                "total_reviews": 1450,
                "emergency_services": True,
                "has_icu": True,
                "has_ambulance": True,
                "is_24x7": True
            },
            {
                "id": "H005",
                "name": "Max Super Specialty Hospital",
                "address": "1, Press Enclave Road, Saket",
                "city": "New Delhi",
                "state": "Delhi",
                "pincode": "110017",
                "latitude": 28.5244,
                "longitude": 77.2066,
                "phone": "+91-11-2651-5050",
                "specialties": ["cardiology", "neurology", "oncology", "orthopedics", "emergency"],
                "rating": 4.5,
                "total_reviews": 1600,
                "emergency_services": True,
                "has_icu": True,
                "has_ambulance": True,
                "is_24x7": True
            }
        ]
        
        for hospital_data in sample_hospitals:
            self.hospitals.append(Hospital(**hospital_data))
        
        print(f"✅ Loaded {len(self.hospitals)} sample hospitals")
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two coordinates using Haversine formula
        Returns distance in kilometers
        """
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        
        # Radius of earth in kilometers
        r = 6371
        
        return c * r
    
    def _get_coordinates_from_location(self, location: str) -> Optional[Tuple[float, float]]:
        """
        Get latitude and longitude from location string using geocoding
        In production, use Google Maps API or similar service
        """
        # For demo purposes, return sample coordinates
        # In production, implement actual geocoding
        city_coords = {
            "chennai": (13.0827, 80.2707),
            "bangalore": (12.9716, 77.5946),
            "delhi": (28.7041, 77.1025),
            "mumbai": (19.0760, 72.8777),
            "kolkata": (22.5726, 88.3639),
            "hyderabad": (17.3850, 78.4867),
            "pune": (18.5204, 73.8567),
            "ahmedabad": (23.0225, 72.5714)
        }
        
        location_lower = location.lower()
        for city, coords in city_coords.items():
            if city in location_lower:
                return coords
        
        # Default to Chennai if location not found
        return (13.0827, 80.2707)
    
    def search_hospitals(
        self,
        location: Optional[str] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        specialty: Optional[str] = None,
        urgency: str = "routine",
        max_distance_km: float = 50.0,
        max_results: int = 10
    ) -> Dict:
        """
        Search for hospitals based on criteria
        
        Args:
            location: City or address string
            latitude: User's latitude
            longitude: User's longitude
            specialty: Required medical specialty
            urgency: 'emergency', 'urgent', or 'routine'
            max_distance_km: Maximum search radius
            max_results: Maximum number of results
            
        Returns:
            Dict with hospitals and metadata
        """
        try:
            # Get user coordinates
            if latitude is None or longitude is None:
                if location:
                    coords = self._get_coordinates_from_location(location)
                    if coords:
                        latitude, longitude = coords
                else:
                    return {
                        "success": False,
                        "error": "Please provide either location or coordinates"
                    }
            
            # Calculate distances
            results = []
            for hospital in self.hospitals:
                distance = self._calculate_distance(
                    latitude, longitude,
                    hospital.latitude, hospital.longitude
                )
                
                # Apply filters
                if distance > max_distance_km:
                    continue
                
                if specialty and specialty.lower() not in hospital.specialties:
                    continue
                
                # For emergency, only show hospitals with emergency services
                if urgency == "emergency" and not hospital.emergency_services:
                    continue
                
                # Create copy with distance
                hospital_copy = Hospital(**hospital.__dict__)
                hospital_copy.distance_km = distance
                results.append(hospital_copy)
            
            # Sort by distance
            results.sort(key=lambda h: h.distance_km)
            
            # Limit results
            results = results[:max_results]
            
            # Generate recommendations
            recommendations = self._generate_recommendations(urgency, len(results))
            
            return {
                "success": True,
                "user_location": {
                    "latitude": latitude,
                    "longitude": longitude,
                    "location_string": location
                },
                "search_criteria": {
                    "specialty": specialty,
                    "urgency": urgency,
                    "max_distance_km": max_distance_km
                },
                "total_results": len(results),
                "hospitals": [h.to_dict() for h in results],
                "recommendations": recommendations,
                "emergency_numbers": self._get_emergency_numbers()
            }
            
        except Exception as e:
            print(f"❌ Hospital search error: {e}")
            return {
                "success": False,
                "error": str(e),
                "hospitals": []
            }
    
    def _generate_recommendations(self, urgency: str, results_count: int) -> List[str]:
        """Generate contextual recommendations"""
        recommendations = []
        
        if urgency == "emergency":
            recommendations.extend([
                "🚨 For life-threatening emergencies, call 108/102 (India) or 911 (US) immediately",
                "📍 Closest hospitals with emergency services are listed first",
                "🚑 If unable to travel, request ambulance service"
            ])
        elif urgency == "urgent":
            recommendations.extend([
                "⏰ Urgent care needed - contact hospitals to check availability",
                "📞 Call ahead to confirm specialists are available",
                "🏥 Consider emergency room if symptoms worsen"
            ])
        else:
            recommendations.extend([
                "📅 Schedule an appointment for non-urgent consultations",
                "🔍 Check hospital reviews and ratings before visiting",
                "💰 Verify insurance acceptance and consultation fees"
            ])
        
        if results_count == 0:
            recommendations.append("⚠️ No hospitals found nearby. Try expanding search radius.")
        
        return recommendations
    
    def _get_emergency_numbers(self) -> Dict:
        """Get emergency contact numbers by country"""
        return {
            "india": {
                "ambulance": "108 / 102",
                "police": "100",
                "fire": "101",
                "women_helpline": "1091",
                "child_helpline": "1098"
            },
            "us": {
                "emergency": "911"
            }
        }
    
    def get_hospital_by_id(self, hospital_id: str) -> Optional[Dict]:
        """Get detailed information for specific hospital"""
        for hospital in self.hospitals:
            if hospital.id == hospital_id:
                return hospital.to_dict()
        return None
    
    def get_specialties_list(self) -> List[Dict]:
        """Get list of available specialties"""
        return [
            {"code": code, "name": name}
            for code, name in self.SPECIALTIES.items()
        ]


# Create global instance
hospital_finder = SmartHospitalFinder()


# Example usage
if __name__ == "__main__":
    print("🏥 Smart Hospital Finder Test\n")
    
    # Test 1: Emergency search in Chennai
    print("Test 1: Emergency search in Chennai")
    result = hospital_finder.search_hospitals(
        location="Chennai",
        urgency="emergency",
        max_distance_km=20
    )
    print(f"Found {result['total_results']} hospitals")
    if result['hospitals']:
        print(f"Nearest: {result['hospitals'][0]['name']} - {result['hospitals'][0]['distance_km']}km\n")
    
    # Test 2: Cardiology specialist search
    print("Test 2: Cardiology specialist in Delhi")
    result = hospital_finder.search_hospitals(
        location="Delhi",
        specialty="cardiology",
        urgency="routine",
        max_distance_km=30
    )
    print(f"Found {result['total_results']} cardiology hospitals\n")
    
    # Test 3: Get available specialties
    print("Test 3: Available specialties")
    specialties = hospital_finder.get_specialties_list()
    print(f"Total specialties: {len(specialties)}")
    for spec in specialties[:5]:
        print(f"  - {spec['name']}")