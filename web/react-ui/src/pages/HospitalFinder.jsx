import React, { useState, useEffect } from "react";
import { MapPin, Navigation, Phone, Star, Clock, Ambulance, Heart, AlertCircle, Filter, Search, Home, Zap, Activity, TrendingUp, Award, CheckCircle } from "lucide-react";

const HospitalFinder = () => {
  const [location, setLocation] = useState("");
  const [userCoords, setUserCoords] = useState(null);
  const [specialty, setSpecialty] = useState("");
  const [urgency, setUrgency] = useState("routine");
  const [hospitals, setHospitals] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedHospital, setSelectedHospital] = useState(null);
  const [showFilters, setShowFilters] = useState(false);
  const [locationLoading, setLocationLoading] = useState(false);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  // Mouse tracking for 3D effect
  useEffect(() => {
    const handleMouseMove = (e) => {
      setMousePos({
        x: (e.clientX / window.innerWidth - 0.5) * 20,
        y: (e.clientY / window.innerHeight - 0.5) * 20
      });
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  const specialties = [
    { code: "general", name: "General Medicine", icon: "🏥" },
    { code: "cardiology", name: "Cardiology", icon: "❤️" },
    { code: "neurology", name: "Neurology", icon: "🧠" },
    { code: "orthopedics", name: "Orthopedics", icon: "🦴" },
    { code: "pediatrics", name: "Pediatrics", icon: "👶" },
    { code: "emergency", name: "Emergency", icon: "🚨" }
  ];

  const urgencyLevels = [
    { value: "emergency", label: "Emergency", color: "from-red-500 to-pink-500", icon: "🚨" },
    { value: "urgent", label: "Urgent", color: "from-orange-500 to-yellow-500", icon: "⚠️" },
    { value: "routine", label: "Routine", color: "from-green-500 to-blue-500", icon: "📅" }
  ];

  // Get user's current location
const getUserLocation = () => {
  setLocationLoading(true);

  if (!navigator.geolocation) {
    alert("Geolocation not supported");
    setLocationLoading(false);
    return;
  }

  navigator.geolocation.getCurrentPosition(
    (position) => {
      setUserCoords({
        latitude: position.coords.latitude,
        longitude: position.coords.longitude
      });

      setLocation(
        `${position.coords.latitude}, ${position.coords.longitude}`
      );

      setLocationLoading(false);
    },
    (error) => {
      console.error(error);
      alert("Location permission denied");
      setLocationLoading(false);
    }
  );
};

const searchHospitals = async () => {
  if (!location.trim()) {
    alert("Please enter a location");
    return;
  }

  setLoading(true);

  try {
    const params = new URLSearchParams({
      location,
      specialty,
      urgency
    });

    const response = await fetch(
      `http://localhost:5050/api/hospitals?${params.toString()}`
    );

    const data = await response.json();

    if (data.success) {
      setHospitals(data.hospitals);
    } else {
      alert(data.error || "No hospitals found");
      setHospitals([]);
    }
  } catch (error) {
    console.error("Search error:", error);
    alert("Backend not reachable");
  } finally {
    setLoading(false);
  }
};



  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 text-white overflow-hidden">
      
      {/* Animated Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div 
          className="absolute w-96 h-96 bg-blue-500/30 rounded-full blur-3xl animate-pulse"
          style={{ top: '10%', left: '10%', transform: `translate(${mousePos.x}px, ${mousePos.y}px)` }}
        />
        <div 
          className="absolute w-96 h-96 bg-pink-500/30 rounded-full blur-3xl animate-pulse"
          style={{ top: '60%', right: '10%', transform: `translate(${-mousePos.x}px, ${-mousePos.y}px)`, animationDelay: '1s' }}
        />
        <div 
          className="absolute w-96 h-96 bg-purple-500/30 rounded-full blur-3xl animate-pulse"
          style={{ bottom: '10%', left: '50%', transform: `translate(${mousePos.y}px, ${mousePos.x}px)`, animationDelay: '2s' }}
        />
        
        {/* Grid pattern */}
        <div className="absolute inset-0 opacity-10"
          style={{
            backgroundImage: 'linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)',
            backgroundSize: '50px 50px'
          }}
        />
      </div>

      {/* Floating medical icons */}
      <div className="fixed inset-0 pointer-events-none">
        {['❤️', '🏥', '💊', '🩺', '🚑'].map((icon, i) => (
          <div
            key={i}
            className="absolute text-4xl opacity-20"
            style={{
              left: `${(i * 20 + 10)}%`,
              top: `${20 + i * 15}%`,
              animation: `float ${8 + i * 2}s ease-in-out infinite`,
              animationDelay: `${i * 0.5}s`
            }}
          >
            {icon}
          </div>
        ))}
      </div>

      <div className="relative z-10 min-h-screen">
        {/* Header */}
        <div className="backdrop-blur-xl bg-white/5 border-b border-white/10 px-6 py-4 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto flex justify-between items-center">
            <div className="flex items-center gap-4">
              <div className="relative">
                <div className="w-14 h-14 bg-gradient-to-br from-blue-500 to-pink-500 rounded-2xl flex items-center justify-center shadow-2xl shadow-blue-500/50 animate-pulse">
                  <Heart className="w-8 h-8 text-white" />
                </div>
                <div className="absolute -bottom-1 -right-1 w-6 h-6 bg-red-500 rounded-full flex items-center justify-center animate-pulse">
                  <Ambulance className="w-3 h-3 text-white" />
                </div>
              </div>
              <div>
                <h1 className="text-2xl font-black bg-gradient-to-r from-blue-400 via-pink-400 to-purple-400 bg-clip-text text-transparent">
                  Smart Hospital Finder
                </h1>
                <p className="text-sm text-gray-400 flex items-center gap-2">
                  <Activity className="w-3 h-3 animate-pulse text-green-400" />
                  Find the best care near you
                </p>
              </div>
            </div>
            <button
              onClick={() => window.history.back()}
              className="px-6 py-3 rounded-xl bg-gradient-to-r from-blue-500 to-purple-500 hover:scale-105 transition-all shadow-lg flex items-center gap-2 font-bold"
            >
              <Home className="w-5 h-5" />
              Back
            </button>
          </div>
        </div>

        {/* Main Content */}
        <div className="max-w-7xl mx-auto px-6 py-8">
          
          {/* Search Section */}
          <div className="mb-8">
            <div className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-xl border-2 border-white/10 rounded-3xl p-8 shadow-2xl">
              
              {/* Emergency Banner */}
              <div className={`mb-6 p-4 rounded-2xl bg-gradient-to-r ${urgencyLevels.find(u => u.value === urgency)?.color} bg-opacity-20 border-2 border-current`}>
                <div className="flex items-center gap-3">
                  <AlertCircle className="w-6 h-6" />
                  <div>
                    <h3 className="font-bold">Emergency? Call 108/102 immediately</h3>
                    <p className="text-sm opacity-80">For life-threatening situations, don't wait - call emergency services</p>
                  </div>
                </div>
              </div>

              {/* Urgency Selector */}
              <div className="mb-6">
                <label className="block text-sm font-bold mb-3">Select Urgency Level</label>
                <div className="grid grid-cols-3 gap-4">
                  {urgencyLevels.map((level) => (
                    <button
                      key={level.value}
                      onClick={() => setUrgency(level.value)}
                      className={`p-4 rounded-2xl border-2 transition-all ${
                        urgency === level.value
                          ? `bg-gradient-to-r ${level.color} border-white/50 scale-105`
                          : 'bg-white/5 border-white/10 hover:bg-white/10'
                      }`}
                    >
                      <div className="text-3xl mb-2">{level.icon}</div>
                      <div className="font-bold">{level.label}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Location Input */}
              <div className="mb-6">
                <label className="block text-sm font-bold mb-3">Your Location</label>
                <div className="flex gap-3">
                  <div className="flex-1 relative">
                    <MapPin className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                    <input
                      type="text"
                      value={location}
                      onChange={(e) => setLocation(e.target.value)}
                      placeholder="Enter city or address..."
                      className="w-full pl-12 pr-4 py-4 rounded-2xl bg-slate-800/50 border-2 border-white/10 focus:border-blue-500 outline-none transition-all"
                    />
                  </div>
                  <button
                    onClick={getUserLocation}
                    disabled={locationLoading}
                    className="px-6 py-4 rounded-2xl bg-gradient-to-r from-blue-500 to-cyan-500 hover:scale-105 transition-all shadow-xl flex items-center gap-2 font-bold disabled:opacity-50"
                  >
                    {locationLoading ? (
                      <div className="w-5 h-5 border-3 border-white/30 border-t-white rounded-full animate-spin" />
                    ) : (
                      <Navigation className="w-5 h-5" />
                    )}
                    Use My Location
                  </button>
                </div>
              </div>

              {/* Specialty Filter */}
              <div className="mb-6">
                <label className="block text-sm font-bold mb-3">Medical Specialty (Optional)</label>
                <div className="grid grid-cols-3 md:grid-cols-6 gap-3">
                  {specialties.map((spec) => (
                    <button
                      key={spec.code}
                      onClick={() => setSpecialty(specialty === spec.code ? "" : spec.code)}
                      className={`p-3 rounded-xl transition-all ${
                        specialty === spec.code
                          ? 'bg-gradient-to-r from-purple-500 to-pink-500 border-2 border-white/50 scale-105'
                          : 'bg-white/5 border-2 border-white/10 hover:bg-white/10'
                      }`}
                    >
                      <div className="text-2xl mb-1">{spec.icon}</div>
                      <div className="text-xs font-semibold">{spec.name.split(' ')[0]}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Search Button */}
              <button
                onClick={searchHospitals}
                disabled={loading}
                className="w-full py-5 rounded-2xl bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 hover:scale-105 transition-all shadow-2xl shadow-blue-500/50 flex items-center justify-center gap-3 font-bold text-lg disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <div className="w-6 h-6 border-3 border-white/30 border-t-white rounded-full animate-spin" />
                    Searching...
                  </>
                ) : (
                  <>
                    <Search className="w-6 h-6" />
                    Find Hospitals
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Results */}
          {hospitals.length > 0 && (
            <div>
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-3xl font-black">
                  Found <span className="text-transparent bg-gradient-to-r from-blue-400 to-pink-400 bg-clip-text">{hospitals.length}</span> Hospitals
                </h2>
                <div className="text-sm text-gray-400 flex items-center gap-2">
                  <TrendingUp className="w-4 h-4" />
                  Sorted by distance
                </div>
              </div>

              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {hospitals.map((hospital, i) => (
                  <div
                    key={hospital.id}
                    onClick={() => setSelectedHospital(hospital)}
                    className="group relative bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-xl border-2 border-white/10 rounded-3xl p-6 hover:scale-105 hover:border-blue-500/50 transition-all duration-500 cursor-pointer shadow-2xl"
                    style={{ animationDelay: `${i * 0.1}s` }}
                  >
                    {/* Distance Badge */}
                    <div className="absolute -top-3 -right-3 bg-gradient-to-r from-blue-500 to-purple-500 px-4 py-2 rounded-full shadow-xl">
                      <div className="flex items-center gap-1 font-bold text-sm">
                        <Navigation className="w-4 h-4" />
                        {hospital.distance_km} km
                      </div>
                    </div>

                    {/* Hospital Info */}
                    <div className="mb-4">
                      <h3 className="text-xl font-black mb-2 group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-blue-400 group-hover:to-pink-400 group-hover:bg-clip-text transition-all">
                        {hospital.name}
                      </h3>
                      <p className="text-sm text-gray-400 mb-3 flex items-start gap-2">
                        <MapPin className="w-4 h-4 mt-0.5 flex-shrink-0" />
                        {hospital.address}, {hospital.city}
                      </p>
                    </div>

                    {/* Rating */}
                    <div className="flex items-center gap-2 mb-4">
                      <div className="flex items-center gap-1 bg-yellow-500/20 px-3 py-1 rounded-full">
                        <Star className="w-4 h-4 text-yellow-400 fill-yellow-400" />
                        <span className="font-bold text-sm">{hospital.rating}</span>
                      </div>
                      {hospital.is_24x7 && (
                        <div className="flex items-center gap-1 bg-green-500/20 px-3 py-1 rounded-full">
                          <Clock className="w-4 h-4 text-green-400" />
                          <span className="text-xs font-semibold text-green-400">24x7</span>
                        </div>
                      )}
                    </div>

                    {/* Features */}
                    <div className="flex flex-wrap gap-2 mb-4">
                      {hospital.emergency_services && (
                        <div className="flex items-center gap-1 bg-red-500/20 px-2 py-1 rounded-lg text-xs">
                          <Ambulance className="w-3 h-3" />
                          Emergency
                        </div>
                      )}
                      {hospital.has_icu && (
                        <div className="flex items-center gap-1 bg-blue-500/20 px-2 py-1 rounded-lg text-xs">
                          <Heart className="w-3 h-3" />
                          ICU
                        </div>
                      )}
                    </div>

                    {/* Actions */}
                    <div className="flex gap-2">
                      <a
                        href={`tel:${hospital.phone}`}
                        className="flex-1 py-3 rounded-xl bg-green-500/20 hover:bg-green-500/30 border border-green-500/50 flex items-center justify-center gap-2 font-bold transition-all"
                        onClick={(e) => e.stopPropagation()}
                      >
                        <Phone className="w-4 h-4" />
                        Call
                      </a>
                      <a
                        href={hospital.google_maps_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex-1 py-3 rounded-xl bg-blue-500/20 hover:bg-blue-500/30 border border-blue-500/50 flex items-center justify-center gap-2 font-bold transition-all"
                        onClick={(e) => e.stopPropagation()}
                      >
                        <MapPin className="w-4 h-4" />
                        Directions
                      </a>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* No Results */}
          {hospitals.length === 0 && location && !loading && (
            <div className="text-center py-20">
              <div className="w-32 h-32 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-6 animate-bounce">
                <Search className="w-16 h-16" />
              </div>
              <h3 className="text-2xl font-bold mb-2">Search for Hospitals</h3>
              <p className="text-gray-400">Enter your location and click "Find Hospitals" to get started</p>
            </div>
          )}
        </div>
      </div>

      <style>{`
        @keyframes float {
          0%, 100% { transform: translateY(0px) rotate(0deg); }
          50% { transform: translateY(-20px) rotate(5deg); }
        }
      `}</style>
    </div>
  );
};

export default HospitalFinder;