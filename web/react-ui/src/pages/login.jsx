import React, { useState } from "react";
import API from "../app/api";
import { useNavigate, Link } from "react-router-dom";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

 const handleLogin = async (e) => {
  e.preventDefault();
  try {
    const res = await API.post("/users/login", { email, password });

    if (res.data.success && res.data.access_token) {
      localStorage.setItem("token", res.data.access_token);
      alert("✅ Login successful!");
      navigate("/");
    }
  } catch (err) {
    console.error(err.response?.data);
    setError(err.response?.data?.detail || "Invalid credentials");
  }
};


  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white">
      <div className="p-10 rounded-2xl bg-white/10 w-96">
        <h1 className="text-3xl font-bold mb-6">Login</h1>
        {error && <div className="mb-4 text-red-400">{error}</div>}
        
        <form onSubmit={handleLogin}>
          <input
            className="w-full p-3 mb-4 rounded bg-black/40"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            className="w-full p-3 mb-4 rounded bg-black/40"
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button className="w-full py-3 bg-green-500 rounded font-bold">
            Login
          </button>
        </form>

        <p className="mt-4 text-center text-gray-400">
          Don't have an account? <Link to="/register" className="text-green-400">Register</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;