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
| **Retrieval Engine | ai_engine.py — matches query to knowledge base        |
| **Relevance Scoring| Farm health score (0–100) based on conditions         |
| **Result Ranking** | Primary, secondary crops ranked by relevance          |
| **External Source**| OpenWeatherMap API (real-time data retrieval)         |

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

**Q: What external API did you use?**
A: OpenWeatherMap API — fetches live temperature, humidity, wind speed, and weather conditions for any city worldwide.

**Q: What is the scoring system?**
A: A relevance score (0–100) calculated by deducting points for irrigation needs and pest risk levels, similar to IR relevance ranking.
