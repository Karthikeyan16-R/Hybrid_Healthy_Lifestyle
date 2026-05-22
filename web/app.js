// app.js
const API_BASE = "http://127.0.0.1:5050"; // backend

function toggleForm(type) {
  document.getElementById("login-box").classList.toggle("active", type === "login");
  document.getElementById("register-box").classList.toggle("active", type === "register");
}

// ---------- REGISTER ----------
async function register() {
  const email = document.getElementById("register-email").value;
  const password = document.getElementById("register-password").value;
  const confirm = document.getElementById("register-confirm").value;

  if (!email || !password || !confirm) {
    alert("Please fill all fields");
    return;
  }

  const response = await fetch(`${API_BASE}/users/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password, confirm_password: confirm }),
  });

  const data = await response.json();
  if (response.ok) {
    alert("✅ Registration successful! You can now log in.");
    toggleForm("login");
  } else {
    alert(`❌ Error: ${data.detail || data.message}`);
  }
}

// ---------- LOGIN ----------
async function login() {
  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;

  if (!email || !password) {
    alert("Please fill all fields");
    return;
  }

  const response = await fetch(`${API_BASE}/users/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  const data = await response.json();

  if (response.ok && data.success) {
    alert("✅ Login successful!");
    localStorage.setItem("token", data.token);
    window.location.href = "home.html"; // redirect to your next page
  } else {
    alert(`❌ Login failed: ${data.detail || data.message}`);
  }
}
