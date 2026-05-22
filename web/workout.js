const API_BASE = "http://127.0.0.1:5050";

async function generateWorkout() {
  const payload = {
    age: Number(age.value),
    height: Number(height.value),
    weight: Number(weight.value),
    goal: "fitness",
    activity_level: activity_level.value,
    time_available: Number(time_available.value)
  };

  try {
    const res = await fetch(`${API_BASE}/ai/workout-fitbit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    document.getElementById("workout-result").innerHTML = `
      <h3>Workout Tier: ${data.plan.WorkoutTier}</h3>
      <p><b>BMI:</b> ${data.plan.BMI}</p>
      <p><b>Main Workout:</b> ${data.plan.WorkoutPlan.main}</p>
    `;

  } catch (err) {
    alert("Workout API not responding");
    console.error(err);
  }
}
