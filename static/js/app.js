/**
 * app.js — Smart Crop Advisory System
 * Handles form submission, API calls, and result rendering
 */

// ─── Utility ──────────────────────────────────────────────────────────────

function updateMoistureDisplay(val) {
  document.getElementById("moisture_val").textContent = val;
}

function showSection(id) {
  ["loadingState", "errorState", "resultsSection"].forEach(s => {
    document.getElementById(s).classList.add("hidden");
  });
  if (id) document.getElementById(id).classList.remove("hidden");
}

function resetForm() {
  showSection(null);
  document.getElementById("advisoryForm").scrollIntoView({ behavior: "smooth" });
}

// ─── Loading step animation ────────────────────────────────────────────────

let loadingInterval = null;

function animateLoadingSteps() {
  const steps = document.querySelectorAll(".ls");
  let current = 0;
  steps.forEach(s => s.classList.remove("active"));
  steps[0].classList.add("active");

  loadingInterval = setInterval(() => {
    current = (current + 1) % steps.length;
    steps.forEach(s => s.classList.remove("active"));
    steps[current].classList.add("active");
  }, 900);
}

function stopLoadingAnimation() {
  if (loadingInterval) {
    clearInterval(loadingInterval);
    loadingInterval = null;
  }
}

// ─── Weather Icon Mapper ───────────────────────────────────────────────────

function getWeatherEmoji(weatherMain) {
  const map = {
    "Clear": "☀️", "Clouds": "⛅", "Rain": "🌧️",
    "Drizzle": "🌦️", "Thunderstorm": "⛈️", "Snow": "❄️",
    "Mist": "🌫️", "Haze": "🌫️", "Fog": "🌫️",
    "Smoke": "💨", "Dust": "🌪️", "Tornado": "🌪️"
  };
  return map[weatherMain] || "🌤️";
}

// ─── Render Weather Card ───────────────────────────────────────────────────

function renderWeather(w) {
  document.getElementById("weatherLocation").textContent =
    `📍 ${w.city}, ${w.country}`;
  document.getElementById("weatherTemp").textContent = `${w.temperature}°C`;
  document.getElementById("weatherDesc").textContent = w.description;
  document.getElementById("weatherIcon").textContent = getWeatherEmoji(w.weather_main);

  document.getElementById("weatherStats").innerHTML = `
    <div class="w-stat">
      <div class="w-stat-label">HUMIDITY</div>
      <div class="w-stat-val">${w.humidity}%</div>
    </div>
    <div class="w-stat">
      <div class="w-stat-label">WIND</div>
      <div class="w-stat-val">${w.wind_speed} m/s</div>
    </div>
    <div class="w-stat">
      <div class="w-stat-label">PRESSURE</div>
      <div class="w-stat-val">${w.pressure} hPa</div>
    </div>
    <div class="w-stat">
      <div class="w-stat-label">FEELS LIKE</div>
      <div class="w-stat-val">${w.feels_like}°C</div>
    </div>
  `;
}

// ─── Render Score ──────────────────────────────────────────────────────────

function renderScore(score) {
  const colors = { "A": "#7aaa50", "B": "#d4880a", "C": "#d4880a", "D": "#c44040" };
  const el = document.getElementById("scoreNum");
  el.textContent = score.score;
  el.style.color = colors[score.grade] || "#7aaa50";

  document.getElementById("scoreGrade").textContent = score.grade;
  document.getElementById("scoreStatus").textContent = `${score.status} Farm Conditions`;
}

// ─── Render Crop Advice ────────────────────────────────────────────────────

function renderCropAdvice(crop) {
  document.getElementById("cropZone").textContent = crop.climate_zone + " Zone";
  document.getElementById("cropReason").textContent = crop.reason;

  // Crop lists
  document.getElementById("cropLists").innerHTML = `
    <div class="crop-list-block primary">
      <h5>✅ Recommended</h5>
      ${crop.primary_crops.map(c => `<span class="crop-tag tag-primary">${c}</span>`).join("")}
    </div>
    <div class="crop-list-block secondary">
      <h5>🔶 Secondary</h5>
      ${crop.secondary_crops.map(c => `<span class="crop-tag tag-secondary">${c}</span>`).join("")}
    </div>
    <div class="crop-list-block avoid">
      <h5>❌ Avoid</h5>
      ${crop.avoid_crops.map(c => `<span class="crop-tag tag-avoid">${c}</span>`).join("")}
    </div>
  `;

  // Soil note
  document.getElementById("soilNote").innerHTML = `
    <div class="label">🪨 Soil Type Adjustment</div>
    <p>${crop.soil_note}</p>
    <div style="margin-top:8px">
      ${crop.soil_bonus.map(c => `<span class="crop-tag tag-soil">${c}</span>`).join("")}
    </div>
  `;

  // Season block
  if (crop.season) {
    document.getElementById("seasonBlock").innerHTML = `
      <div class="label">📅 Current Season</div>
      <div class="season-name">${crop.season.name} Season</div>
      <div class="season-months">${crop.season.months}</div>
      ${crop.season.crops.map(c => `<span class="crop-tag tag-secondary">${c}</span>`).join("")}
    `;
  } else {
    document.getElementById("seasonBlock").innerHTML = "";
  }
}

// ─── Render Irrigation ─────────────────────────────────────────────────────

function renderIrrigation(irr) {
  const levelClass = "level-" + irr.color.toLowerCase().replace(/ /g, "-");
  document.getElementById("irrigationLevel").innerHTML =
    `<span class="${levelClass}">${irr.icon} ${irr.level}</span>`;

  document.getElementById("irrigationBody").innerHTML = `
    <div class="irr-action">${irr.action}</div>

    <div class="moisture-bar-wrap">
      <div class="mb-label">
        <span>Soil Moisture</span>
        <span>${irr.moisture_bar}%</span>
      </div>
      <div class="moisture-bar-bg">
        <div class="moisture-bar-fill" style="width: ${irr.moisture_bar}%; background: ${getMoistureColor(irr.moisture_bar)}"></div>
      </div>
    </div>

    <div class="irr-details">
      <div class="irr-row">
        <span class="irr-key">Frequency:</span>
        <span class="irr-val">${irr.frequency}</span>
      </div>
      <div class="irr-row">
        <span class="irr-key">Amount:</span>
        <span class="irr-val">${irr.amount}</span>
      </div>
      <div class="irr-row">
        <span class="irr-key">Method:</span>
        <span class="irr-val">${irr.method}</span>
      </div>
    </div>

    <div class="irr-tip">💡 ${irr.tip}</div>
  `;
}

function getMoistureColor(val) {
  if (val < 25) return "linear-gradient(90deg, #c44040, #e05050)";
  if (val < 45) return "linear-gradient(90deg, #d4880a, #f0a820)";
  if (val < 70) return "linear-gradient(90deg, #5a7a3a, #7aaa50)";
  return "linear-gradient(90deg, #2a7a6a, #3aa090)";
}

// ─── Render Pest Advice ────────────────────────────────────────────────────

function renderPest(pest) {
  const levelClass = "level-" + pest.color.toLowerCase().replace(/ /g, "-");
  document.getElementById("pestLevel").innerHTML =
    `<span class="${levelClass}">${pest.icon} ${pest.level} Risk</span>`;

  document.getElementById("pestBody").innerHTML = `
    <div class="pest-action">${pest.action}</div>

    <div class="pest-section-label">⚠️ Likely Pests</div>
    <div>
      ${pest.pests.map(p => `<span class="crop-tag tag-avoid">${p}</span>`).join("")}
    </div>

    <div class="pest-section-label">🦠 Disease Risks</div>
    <div>
      ${pest.diseases.map(d => `<span class="crop-tag tag-secondary">${d}</span>`).join("")}
    </div>

    <div class="pest-section-label">🛡️ Prevention Steps</div>
    <div class="prevention-list">
      ${pest.prevention.map(p => `
        <div class="prev-item">
          <div class="prev-dot"></div>
          <span>${p}</span>
        </div>
      `).join("")}
    </div>
  `;
}

// ─── Render IR Pipeline ────────────────────────────────────────────────────

function renderIRPipeline(weather, advice) {
  const q = advice.query_params;
  document.getElementById("irPipeline").innerHTML = `
    <div class="ir-step">
      <div class="ir-step-num">Step 01</div>
      <div class="ir-step-title">Query Formulation</div>
      <div class="ir-step-desc">User inputs converted into structured IR query parameters</div>
      <div class="ir-step-val">City: ${weather.city} | Moisture: ${q.soil_moisture}% | Soil: ${q.soil_type}</div>
    </div>
    <div class="ir-step">
      <div class="ir-step-num">Step 02</div>
      <div class="ir-step-title">Data Retrieval</div>
      <div class="ir-step-desc">Real-time weather data fetched from OpenWeatherMap API</div>
      <div class="ir-step-val">${weather.temperature}°C | ${weather.humidity}% Humidity | ${weather.description}</div>
    </div>
    <div class="ir-step">
      <div class="ir-step-num">Step 03</div>
      <div class="ir-step-title">Index Lookup</div>
      <div class="ir-step-desc">Climate zone mapped to crop & pest knowledge base</div>
      <div class="ir-step-val">Zone: ${advice.crop.climate_zone}</div>
    </div>
    <div class="ir-step">
      <div class="ir-step-num">Step 04</div>
      <div class="ir-step-title">Relevance Ranking</div>
      <div class="ir-step-desc">Advisory rules scored by relevance to query conditions</div>
      <div class="ir-step-val">Score: ${advice.score.score}/100 — ${advice.score.status}</div>
    </div>
    <div class="ir-step">
      <div class="ir-step-num">Step 05</div>
      <div class="ir-step-title">Result Presentation</div>
      <div class="ir-step-desc">Top-ranked results displayed as structured advisories</div>
      <div class="ir-step-val">Irrigation: ${advice.irrigation.level} | Pest: ${advice.pest.level}</div>
    </div>
  `;
}

// ─── Main Analyze Function ─────────────────────────────────────────────────

async function analyzeData() {
  const city = document.getElementById("city").value.trim();
  const soil_moisture = parseFloat(document.getElementById("soil_moisture").value);
  const soil_type = document.getElementById("soil_type").value;
  const farm_size = document.getElementById("farm_size").value;

  if (!city) {
    document.getElementById("city").focus();
    document.getElementById("city").style.borderColor = "#c44040";
    setTimeout(() => { document.getElementById("city").style.borderColor = ""; }, 2000);
    return;
  }

  // Show loading
  showSection("loadingState");
  animateLoadingSteps();
  window.scrollTo({ top: document.getElementById("loadingState").offsetTop - 80, behavior: "smooth" });

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ city, soil_moisture, soil_type, farm_size })
    });

    const data = await response.json();
    stopLoadingAnimation();

    if (!data.success) {
      document.getElementById("errorTitle").textContent = "Query Failed";
      document.getElementById("errorMessage").textContent = data.error || "An unexpected error occurred.";
      showSection("errorState");
      return;
    }

    // Render everything
    renderWeather(data.weather);
    renderScore(data.advice.score);
    renderCropAdvice(data.advice.crop);
    renderIrrigation(data.advice.irrigation);
    renderPest(data.advice.pest);
    renderIRPipeline(data.weather, data.advice);

    showSection("resultsSection");
    window.scrollTo({ top: document.getElementById("resultsSection").offsetTop - 80, behavior: "smooth" });

  } catch (err) {
    stopLoadingAnimation();
    document.getElementById("errorTitle").textContent = "Network Error";
    document.getElementById("errorMessage").textContent = "Could not connect to the server. Please ensure Flask is running.";
    showSection("errorState");
  }
}

// ─── Allow Enter key to submit ─────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("city").addEventListener("keydown", (e) => {
    if (e.key === "Enter") analyzeData();
  });
});
