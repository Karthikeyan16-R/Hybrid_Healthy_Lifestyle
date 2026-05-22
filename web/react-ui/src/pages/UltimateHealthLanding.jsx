import React, { useState, useEffect } from 'react';
import { Salad, Dumbbell, MessageCircle, Hospital, Trophy, Target, Zap, Heart, Activity, ArrowRight, Play, Star, Sparkles, Brain, Calendar, ChefHat, LineChart } from 'lucide-react';
import { useNavigate } from "react-router-dom";

const UltimateHealthLanding = () => {
  const navigate = useNavigate();
  const [scrollY, setScrollY] = useState(0);
  const [activeTab, setActiveTab] = useState(0);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // Check if user is logged in
  useEffect(() => {
    const token = localStorage.getItem("token");
    setIsLoggedIn(!!token);
  }, []);

  // Auto-rotate hero images
  useEffect(() => {
    const interval = setInterval(() => {
      setActiveTab((prev) => (prev + 1) % heroImages.length);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  // Handle scroll for parallax
  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Handle feature click - Check auth before navigating
  const handleFeatureClick = (route) => {
    if (isLoggedIn) {
      navigate(route);
    } else {
      // Store intended destination and redirect to login
      localStorage.setItem('intendedRoute', route);
      navigate('/login');
    }
  };

  const features = [
    {
      icon: <Salad className="w-12 h-12" />,
      title: "AI Diet Planner",
      desc: "Personalized meal plans based on your goals, allergies & preferences",
      color: "from-green-400 to-emerald-600",
      stat: "Smart Plans",
      image: "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=600&h=400&fit=crop",
      route: "/diet"
    },
    {
      icon: <Dumbbell className="w-12 h-12" />,
      title: "Smart Workouts",
      desc: "Adaptive fitness routines powered by real-time data analysis",
      color: "from-orange-400 to-red-600",
      stat: "AI Powered",
      image: "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600&h=400&fit=crop",
      route: "/workout"
    },
    {
      icon: <MessageCircle className="w-12 h-12" />,
      title: "Health Chatbot",
      desc: "24/7 AI assistant for nutrition, fitness & lifestyle queries",
      color: "from-blue-400 to-indigo-600",
      stat: "Always On",
      image: "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=600&h=400&fit=crop",
      route: "/chat"
    },
    {
      icon: <Hospital className="w-12 h-12" />,
      title: "Hospital Finder",
      desc: "Locate nearby verified hospitals & specialists instantly",
      color: "from-pink-400 to-rose-600",
      stat: "Instant Search",
      image: "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=600&h=400&fit=crop",
      route: "/hospital"
    },
    {
      icon: <Trophy className="w-12 h-12" />,
      title: "30/60 Day Challenges",
      desc: "Gamified fitness goals with rewards & community support",
      color: "from-yellow-400 to-amber-600",
      stat: "Get Motivated",
      image: "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=600&h=400&fit=crop",
      route: "/challenges"
    },
    {
      icon: <Activity className="w-12 h-12" />,
      title: "Progress Analytics",
      desc: "Track calories, macros, workouts & health metrics",
      color: "from-purple-400 to-violet-600",
      stat: "Real-time",
      image: "https://images.unsplash.com/photo-1551963831-b3b1ca40c98e?w=600&h=400&fit=crop",
      route: "/analytics"
    }
  ];

  const heroImages = [
    "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=800&h=1000&fit=crop",
    "https://images.unsplash.com/photo-1574680096145-d05b474e2155?w=800&h=1000&fit=crop",
    "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800&h=1000&fit=crop"
  ];

  const foodGallery = [
    { img: "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500&h=500&fit=crop", label: "Breakfast Bowl", cal: "420 cal" },
    { img: "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=500&h=500&fit=crop", label: "Fresh Salad", cal: "280 cal" },
    { img: "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=500&h=500&fit=crop", label: "Protein Bowl", cal: "520 cal" },
    { img: "https://images.unsplash.com/photo-1511690656952-34342bb7c2f2?w=500&h=500&fit=crop", label: "Power Smoothie", cal: "310 cal" },
    { img: "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=500&h=500&fit=crop", label: "Healthy Pizza", cal: "480 cal" },
    { img: "https://images.unsplash.com/photo-1623428187969-5da2dcea5ebf?w=500&h=500&fit=crop", label: "Veggie Wrap", cal: "390 cal" },
    { img: "https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=500&h=500&fit=crop", label: "Pasta Delight", cal: "550 cal" },
    { img: "https://images.unsplash.com/photo-1606787366850-de6330128bfc?w=500&h=500&fit=crop", label: "Berry Parfait", cal: "260 cal" }
  ];

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("intendedRoute");
    setIsLoggedIn(false);
    navigate("/");
  };

  const handleGetStarted = () => {
    if (isLoggedIn) {
      // Scroll to features section
      const featuresSection = document.getElementById('features-section');
      if (featuresSection) {
        featuresSection.scrollIntoView({ behavior: 'smooth' });
      }
    } else {
      navigate('/register');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white overflow-hidden">
      
      {/* Animated Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div 
          className="absolute w-96 h-96 bg-purple-500/30 rounded-full blur-3xl -top-20 -left-20"
          style={{ transform: `translateY(${scrollY * 0.5}px)` }}
        />
        <div 
          className="absolute w-96 h-96 bg-blue-500/30 rounded-full blur-3xl top-40 right-0"
          style={{ transform: `translateY(${scrollY * 0.3}px)` }}
        />
      </div>

      {/* Navbar */}
      <nav className="relative z-50 px-6 py-4 backdrop-blur-md bg-white/5 border-b border-white/10">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-2 cursor-pointer" onClick={() => navigate('/')}>
            <div className="w-10 h-10 bg-gradient-to-br from-green-400 to-blue-500 rounded-lg flex items-center justify-center">
              <Heart className="w-6 h-6" />
            </div>
            <span className="text-2xl font-bold bg-gradient-to-r from-green-400 to-blue-500 bg-clip-text text-transparent">
              HealthAI
            </span>
          </div>
          <div className="flex gap-4">
            {isLoggedIn ? (
              <>
                <button
                  onClick={() => navigate("/")}
                  className="px-6 py-2 rounded-lg border border-white/20 hover:bg-white/10 transition-all"
                >
                  Home
                </button>
                <button
                  onClick={handleLogout}
                  className="px-6 py-2 rounded-lg bg-gradient-to-r from-red-500 to-pink-500 hover:scale-105 transition-transform"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <button
                  onClick={() => navigate("/login")}
                  className="px-6 py-2 rounded-lg border border-white/20 hover:bg-white/10 transition-all"
                >
                  Login
                </button>
                <button
                  onClick={() => navigate("/register")}
                  className="px-6 py-2 rounded-lg bg-gradient-to-r from-green-500 to-blue-500 hover:scale-105 transition-transform shadow-lg shadow-blue-500/50"
                >
                  Get Started
                </button>
              </>
            )}
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="relative z-10">
        <div className="relative h-[800px] overflow-hidden">
          <div className="absolute inset-0">
            {heroImages.map((img, i) => (
              <img 
                key={i}
                src={img}
                alt="Fitness hero"
                className={`absolute inset-0 w-full h-full object-cover transition-opacity duration-1000 ${i === activeTab ? 'opacity-100' : 'opacity-0'}`}
              />
            ))}
            <div className="absolute inset-0 bg-gradient-to-r from-black via-black/70 to-transparent" />
            <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent" />
          </div>

          <div className="relative max-w-7xl mx-auto px-6 h-full flex items-center">
            <div className="max-w-2xl">
              <div className="inline-block mb-6">
                <div className="flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r from-green-500/20 to-blue-500/20 border border-green-500/30 backdrop-blur-sm animate-pulse">
                  <Sparkles className="w-4 h-4 text-yellow-400" />
                  <span className="text-sm font-semibold">AI-Powered Health Revolution</span>
                </div>
              </div>
              
              <h1 className="text-6xl md:text-8xl font-black mb-6 leading-tight">
                Transform
                <br />
                Your
                <br />
                <span className="bg-gradient-to-r from-green-400 via-blue-500 to-purple-500 bg-clip-text text-transparent">
                  Lifestyle
                </span>
              </h1>
              
              <p className="text-2xl text-gray-200 mb-8 leading-relaxed">
                Experience the future of health with AI-powered personalized diet plans, 
                smart workouts, and 24/7 guidance
              </p>

              <div className="flex flex-col sm:flex-row gap-4">
                <button 
                  onClick={handleGetStarted}
                  className="group px-10 py-5 bg-gradient-to-r from-green-500 to-blue-500 rounded-2xl text-xl font-bold hover:scale-105 transition-all shadow-2xl shadow-blue-500/50 flex items-center justify-center gap-2"
                >
                  {isLoggedIn ? 'Explore Features' : 'Start Free Trial'}
                  <Target className="w-6 h-6 group-hover:rotate-90 transition-transform" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Grid */}
      <div id="features-section" className="relative z-10 max-w-7xl mx-auto px-6 py-32">
        <div className="text-center mb-20">
          <h2 className="text-6xl md:text-7xl font-black mb-6">
            Everything You Need
            <br />
            <span className="bg-gradient-to-r from-pink-400 via-purple-500 to-orange-500 bg-clip-text text-transparent">
              In One Platform
            </span>
          </h2>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, i) => (
            <div
              key={i}
              onClick={() => handleFeatureClick(feature.route)}
              className="group relative rounded-3xl bg-slate-800/50 backdrop-blur-lg border-2 border-white/10 hover:scale-105 hover:shadow-2xl hover:border-white/30 transition-all duration-500 cursor-pointer overflow-hidden"
            >
              <div className="relative h-56 overflow-hidden">
                <img 
                  src={feature.image} 
                  alt={feature.title}
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
                />
                <div className={`absolute inset-0 bg-gradient-to-t ${feature.color} opacity-50 group-hover:opacity-70 transition-opacity`} />
                <div className={`absolute top-6 right-6 w-20 h-20 rounded-2xl bg-gradient-to-br ${feature.color} flex items-center justify-center shadow-2xl group-hover:rotate-12 transition-transform duration-500`}>
                  {feature.icon}
                </div>
              </div>
              
              <div className="p-8">
                <h3 className="text-3xl font-bold mb-4">{feature.title}</h3>
                <p className="text-gray-300 text-lg mb-6">{feature.desc}</p>
                
                <div className="flex items-center justify-between pt-4 border-t border-white/10">
                  <span className="text-sm font-bold text-transparent bg-gradient-to-r from-green-400 to-blue-500 bg-clip-text">{feature.stat}</span>
                  <div className="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center group-hover:bg-gradient-to-r group-hover:from-green-500 group-hover:to-blue-500 transition-all">
                    <ArrowRight className="w-6 h-6" />
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Food Gallery */}
      <div className="relative z-10 bg-gradient-to-b from-transparent via-green-900/20 to-transparent py-32">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-6xl font-black mb-6">
              <span className="bg-gradient-to-r from-green-400 to-emerald-500 bg-clip-text text-transparent">
                Delicious & Nutritious
              </span>
            </h2>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {foodGallery.map((item, i) => (
              <div key={i} className="relative rounded-3xl overflow-hidden group cursor-pointer h-80 border-2 border-white/10 hover:scale-105 transition-all">
                <img 
                  src={item.img}
                  alt={item.label}
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black via-black/40 to-transparent" />
                <div className="absolute bottom-0 left-0 right-0 p-6">
                  <div className="font-bold text-xl">{item.label}</div>
                  <div className="text-green-400 text-sm">{item.cal}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA */}
      <div className="relative z-10 max-w-7xl mx-auto px-6 py-20">
        <div className="text-center p-24 rounded-3xl bg-gradient-to-r from-green-500 to-blue-500">
          <h2 className="text-6xl font-black mb-8">Start Your Journey Today</h2>
          <button 
            onClick={handleGetStarted}
            className="px-16 py-6 bg-white text-blue-600 rounded-2xl text-2xl font-black hover:scale-105 transition-transform"
          >
            Get Started Free
          </button>
        </div>
      </div>

      {/* Footer */}
      <footer className="relative z-10 border-t border-white/10 py-16">
        <div className="max-w-7xl mx-auto px-6 text-center text-gray-400">
          © 2025 HealthAI. Built with ❤️ for your wellness journey.
        </div>
      </footer>
    </div>
  );
};

export default UltimateHealthLanding;