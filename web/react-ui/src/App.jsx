import { BrowserRouter, Routes, Route } from "react-router-dom";

import UltimateHealthLanding from "./pages/UltimateHealthLanding";
import Login from "./pages/Login";
import Register from "./pages/Register";
import DietPlanner from "./pages/DietPlanner";
import Workout from "./pages/Workout";
import Chatbot from "./pages/Chatbot";

import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* 🌍 Public Landing */}
        <Route path="/" element={<UltimateHealthLanding />} />

        {/* 🔓 Auth */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route
          path="/diet"
          element={
            <ProtectedRoute>
              <DietPlanner />
            </ProtectedRoute>
          }
        />

        <Route
          path="/workout"
          element={
            <ProtectedRoute>
              <Workout />
            </ProtectedRoute>
          }
        />

        <Route
          path="/chat"
          element={
            <ProtectedRoute>
              <Chatbot />
            </ProtectedRoute>
          }
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;
