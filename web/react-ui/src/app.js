// src/App.js
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import UltimateHealthLanding from "./pages/UltimateHealthLanding";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import DietPlanner from "./pages/DietPlanner";
import Workout from "./pages/Workout";
import Chatbot from "./pages/Chatbot";
import ospitalFinder from "./pages/ospitalFinder"; // ✅ ADD THIS
import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<UltimateHealthLanding />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        <Route path="/dashboard" element={
          <ProtectedRoute><Dashboard /></ProtectedRoute>
        } />
        
        <Route path="/diet" element={
          <ProtectedRoute><DietPlanner /></ProtectedRoute>
        } />
        
        <Route path="/workout" element={
          <ProtectedRoute><Workout /></ProtectedRoute>
        } />
        
        <Route path="/chat" element={
          <ProtectedRoute><Chatbot /></ProtectedRoute>
        } />
        
        {/* ✅ ADD THIS ROUTE */}
        <Route path="/hospital" element={
          <ProtectedRoute><HospitalFinder /></ProtectedRoute>
        } />
        
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;