import React, { useState } from "react";
import API from "../app/api";
import { useNavigate, Link } from "react-router-dom";

const Register = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    
    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    try {
      const res = await API.post("/users/register", {
        email,
        password,
        confirm_password: confirmPassword
      });
      
      if (res.data.success) {
        alert("✅ Registration successful! Please login.");
        navigate("/login");
      }
    } catch (err) {
      setError("Registration failed. Email might already exist.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white">
      <div className="p-10 rounded-2xl bg-white/10 w-96">
        <h1 className="text-3xl font-bold mb-6">Create Account</h1>
        {error && <div className="mb-4 text-red-400">{error}</div>}
        
        <form onSubmit={handleRegister}>
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
          <input
            className="w-full p-3 mb-4 rounded bg-black/40"
            type="password"
            placeholder="Confirm Password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
          <button className="w-full py-3 bg-green-500 rounded font-bold">
            Register
          </button>
        </form>

        <p className="mt-4 text-center text-gray-400">
          Already have an account? <Link to="/login" className="text-green-400">Login</Link>
        </p>
      </div>
    </div>
  );
};

export default Register;