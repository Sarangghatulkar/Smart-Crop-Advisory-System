# 🌾 Smart Crop Advisory System
## IR (Information Retrieval) College Project

---

## 📁 Folder Structure

```
smart_crop_advisory/
│
├── app.py                  # Flask backend & API integration
├── ai_engine.py            # IR-based AI advisory engine
├── requirements.txt        # Python dependencies
├── README.md               # This file
│
├── templates/
│   └── index.html          # Main HTML page
│
└── static/
    ├── css/
    │   └── style.css       # Professional stylesheet
    └── js/
        └── app.js          # Frontend JavaScript
```

---

## ⚙️ Step-by-Step Installation Guide

### Step 1: Install Python
Make sure Python 3.8+ is installed.
```bash
python --version
```

### Step 2: Get Free OpenWeatherMap API Key
1. Go to https://openweathermap.org/api
2. Click "Sign Up" and create a free account
3. Go to "My API Keys" in your dashboard
4. Copy your API key

### Step 3: Set Your API Key
Open `app.py` and replace line:
```python
WEATHER_API_KEY = "YOUR_API_KEY_HERE"
```
With your actual API key:
```python
WEATHER_API_KEY = "abc123youractualkey456"
```

### Step 4: Install Dependencies
Open terminal/command prompt in the project folder:
```bash
pip install -r requirements.txt
```
Or install manually:
```bash
pip install flask requests
```

### Step 5: Run the Application
```bash
python app.py
```

### Step 6: Open in Browser
Go to: http://127.0.0.1:5000

---

## 🚀 How to Use

1. Enter your **City Name** (e.g., Pune, Mumbai, Delhi)
2. Set **Soil Moisture** percentage using the slider
3. Select your **Soil Type** and **Farm Size**
4. Click **"Analyze & Get Advisory"**
5. View real-time weather + AI advisory results

---

## 🔬 How This Relates to IR (Information Retrieval)

### IR System Mapping:

| IR Component       | This System                                           |
|--------------------|-------------------------------------------------------|
| **Query**          | User input: city + soil moisture + soil type          |
| **Document Index** | Crop/irrigation/pest knowledge base (Python dicts)    |
| **Retrieval Engine** | ai_engine.py — matches query to knowledge base     |
| **Relevance Scoring** | Farm health score (0–100) based on conditions     |
| **Result Ranking** | Primary, secondary crops ranked by relevance         |
| **External Source** | OpenWeatherMap API (real-time data retrieval)        |

### IR Pipeline (5 Steps):
1. **Query Formulation** → User inputs structured into query parameters
2. **Data Retrieval** → Weather API fetches real-world environmental data
3. **Index Lookup** → Climate zone mapped to crop/pest knowledge base
4. **Relevance Ranking** → Advisory rules scored against current conditions
5. **Result Presentation** → Top-ranked advisories displayed to user

### Why This is an IR System:
- It **retrieves relevant information** from a structured knowledge base
- It uses **real-time external data sources** (OpenWeatherMap API)
- It applies **query matching** logic to return ranked results
- It demonstrates **precision and recall** — only relevant crops shown
- The AI engine acts as an **inverted index** — maps conditions to advice

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python 3  | Core backend logic |
| Flask     | Web framework / routing |
| HTML5/CSS3 | Frontend UI |
| JavaScript | Frontend interactions |
| OpenWeatherMap API | Real-time weather data |
| Rule-based AI | Crop/irrigation/pest advisory |

---

## 📋 Project Features

- ✅ Real-time weather fetching
- ✅ Crop recommendation (primary, secondary, avoid)
- ✅ Irrigation advice with soil moisture visualization
- ✅ Pest risk assessment with prevention steps
- ✅ Farm health score (A/B/C/D grade)
- ✅ IR pipeline visualization
- ✅ Season recommendations (Kharif/Rabi/Zaid)
- ✅ Soil type adjustments
- ✅ Professional dark-mode UI
- ✅ Responsive design
- ✅ Error handling

---

## 🎓 For Viva Questions

**Q: What is an IR system?**
A: A system that retrieves relevant information from a collection in response to a user query.

**Q: How does your project use IR?**
A: The user's query (city + soil data) is matched against a knowledge base of agricultural rules. Real-time weather data is retrieved via API. The AI engine ranks and returns the most relevant crop/irrigation/pest advice.

**Q: What is your knowledge base?**
A: Python dictionaries in ai_engine.py containing crop rules indexed by climate zone, irrigation rules indexed by moisture thresholds, and pest rules indexed by temperature/humidity combinations.

**Q: What external API did you use?**
A: OpenWeatherMap API — fetches live temperature, humidity, wind speed, and weather conditions for any city worldwide.

**Q: What is the scoring system?**
A: A relevance score (0–100) calculated by deducting points for irrigation needs and pest risk levels, similar to IR relevance ranking.
