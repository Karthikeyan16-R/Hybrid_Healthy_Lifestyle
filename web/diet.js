const API_BASE = "http://127.0.0.1:5050";

function logout() {
  localStorage.removeItem("token");
  window.location.href = "home.html";
}

async function generateDiet() {
  const age = document.getElementById("age").value;
  const weight = document.getElementById("weight").value;
  const height = document.getElementById("height").value;
  const gender = document.getElementById("gender").value;
  const activity = document.getElementById("activity").value;
  const goal = document.getElementById("goal").value;
  const cuisine = document.getElementById("cuisine").value;

  if (!age || !weight || !height) {
    alert("Please fill in all fields");
    return;
  }

  // ⛔ NO ALLERGIES FIELD ANYMORE
  const payload = {
    age: parseInt(age),
    weight: parseFloat(weight),
    height: parseFloat(height),
    gender,
    activity_level: activity,
    goal,
    cuisine_preference: cuisine
  };

  try {
    const res = await fetch(`${API_BASE}/ai/diet`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (res.ok && data.plan) {
      displayDiet(data.plan);
    } else {
      alert("⚠️ Failed: " + (data.message || data.error || "Unknown error"));
    }
  } catch (error) {
    console.error(error);
    alert("🚨 Backend not responding!");
  }
}

function displayDiet(plan) {
  const output = document.getElementById("plan-output");
  document.getElementById("diet-result").style.display = "block";

  output.innerHTML = `
    <h3>🎯 Daily Calorie Target: ${plan.daily_targets?.calories}</h3>
    <h4>Protein Target: ${plan.daily_targets?.protein} g</h4>

    ${Object.entries(plan.meal_plan).map(
      ([meal, details]) => `
      <div class="meal-box">
        <h3>${meal.toUpperCase()}</h3>
        <p><strong>Target:</strong> ${details.target_calories} kcal | ${details.target_protein} g protein</p>
        <ul>
          ${details.foods
            .map(
              f =>
                `<li>${f.name} — ${f.calories} kcal | P: ${f.protein}g | C: ${f.carbs}g | F: ${f.fat}g</li>`
            )
            .join("")}
        </ul>
      </div>
    `
    ).join("")}
  `;
}
