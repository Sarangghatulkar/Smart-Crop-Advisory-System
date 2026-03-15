"""
ai_engine.py - Smart Crop Advisory AI Engine
============================================
This module implements the Information Retrieval (IR) logic for the
Smart Crop Advisory System. It applies rule-based and condition-based
AI reasoning to generate crop, irrigation, and pest risk advice.

IR Concept Used:
- Query = {city, soil_moisture, soil_type, farm_size}
- Knowledge Base = crop rules, irrigation thresholds, pest conditions
- Retrieval = pattern matching against structured knowledge base
- Output = ranked, relevant advisory results
"""


class CropAdvisoryEngine:
    """
    AI Engine using rule-based IR logic.
    Retrieves relevant crop advice from a structured knowledge base
    based on environmental query parameters.
    """

    # ─── Knowledge Base (IR Document Collection) ───────────────────────────────

    CROP_KNOWLEDGE_BASE = {
        "hot_dry": {
            "primary": ["Millets", "Sorghum", "Sunflower"],
            "secondary": ["Groundnut", "Sesame", "Cowpea"],
            "avoid": ["Wheat", "Spinach", "Lettuce"],
            "reason": "High temperature and low humidity favor drought-resistant crops."
        },
        "hot_humid": {
            "primary": ["Rice", "Sugarcane", "Jute"],
            "secondary": ["Banana", "Coconut", "Taro"],
            "avoid": ["Barley", "Oats", "Mustard"],
            "reason": "Warm and moist conditions are ideal for tropical crops."
        },
        "mild_dry": {
            "primary": ["Wheat", "Barley", "Mustard"],
            "secondary": ["Chickpea", "Lentil", "Peas"],
            "avoid": ["Rice", "Sugarcane"],
            "reason": "Moderate temperature with low humidity suits Rabi season crops."
        },
        "mild_humid": {
            "primary": ["Tomato", "Potato", "Cabbage"],
            "secondary": ["Cauliflower", "Peas", "Beans"],
            "avoid": ["Cotton", "Sorghum"],
            "reason": "Mild and moist conditions are perfect for vegetable crops."
        },
        "cold_dry": {
            "primary": ["Barley", "Rye", "Turnip"],
            "secondary": ["Spinach", "Garlic", "Onion"],
            "avoid": ["Rice", "Maize", "Cotton"],
            "reason": "Cold dry conditions suit hardy winter crops."
        },
        "cold_humid": {
            "primary": ["Peas", "Lettuce", "Kale"],
            "secondary": ["Broccoli", "Brussels Sprouts", "Radish"],
            "avoid": ["Maize", "Sorghum", "Sunflower"],
            "reason": "Cool moist conditions favor leafy greens and cool-season vegetables."
        },
        "rainy": {
            "primary": ["Rice", "Maize", "Jute"],
            "secondary": ["Arrowroot", "Yam", "Taro"],
            "avoid": ["Wheat", "Mustard", "Sesame"],
            "reason": "Heavy rainfall is best suited for Kharif (rain-fed) crops."
        }
    }

    SOIL_ADJUSTMENTS = {
        "sandy": {
            "bonus": ["Groundnut", "Carrot", "Cassava", "Watermelon"],
            "note": "Sandy soil has good drainage; prefer deep-rooted or drought-tolerant crops."
        },
        "clayey": {
            "bonus": ["Rice", "Wheat", "Sugarcane"],
            "note": "Clay soil retains moisture well; suitable for water-intensive crops."
        },
        "loamy": {
            "bonus": ["Maize", "Tomato", "Potato", "Soybean"],
            "note": "Loamy soil is ideal for most crops due to balanced drainage and nutrients."
        },
        "silty": {
            "bonus": ["Wheat", "Vegetables", "Fruits"],
            "note": "Silty soil is fertile and moisture-retentive; great for most crops."
        }
    }

    # ─── Irrigation Knowledge Base ──────────────────────────────────────────────

    IRRIGATION_RULES = [
        {
            "condition": lambda sm, hum, temp: sm < 20 and hum < 40,
            "level": "Critical",
            "icon": "🚨",
            "color": "critical",
            "action": "Immediate irrigation required",
            "frequency": "Irrigate every 1–2 days",
            "amount": "50–60 mm per session",
            "method": "Drip or sprinkler irrigation recommended",
            "tip": "Check for wilting signs in crops. Consider mulching to conserve moisture."
        },
        {
            "condition": lambda sm, hum, temp: sm < 35 or hum < 50,
            "level": "High",
            "icon": "⚠️",
            "color": "high",
            "action": "Irrigation needed soon",
            "frequency": "Irrigate every 2–3 days",
            "amount": "35–45 mm per session",
            "method": "Drip irrigation preferred for water efficiency",
            "tip": "Monitor soil moisture daily. Irrigate in early morning to reduce evaporation."
        },
        {
            "condition": lambda sm, hum, temp: sm < 55 or (hum < 60 and temp > 30),
            "level": "Moderate",
            "icon": "💧",
            "color": "moderate",
            "action": "Irrigation recommended",
            "frequency": "Irrigate every 3–4 days",
            "amount": "25–35 mm per session",
            "method": "Furrow or sprinkler irrigation suitable",
            "tip": "Check evapotranspiration rates. Adjust based on crop growth stage."
        },
        {
            "condition": lambda sm, hum, temp: sm >= 55 and sm < 75,
            "level": "Low",
            "icon": "✅",
            "color": "low",
            "action": "Soil moisture is adequate",
            "frequency": "Irrigate every 5–7 days",
            "amount": "15–25 mm per session",
            "method": "Any standard irrigation method is suitable",
            "tip": "Maintain current moisture levels. Watch for weather forecast changes."
        },
        {
            "condition": lambda sm, hum, temp: sm >= 75,
            "level": "No Irrigation",
            "icon": "🌊",
            "color": "none",
            "action": "No irrigation needed",
            "frequency": "Monitor and wait",
            "amount": "0 mm — soil is sufficiently moist",
            "method": "Ensure proper drainage to prevent waterlogging",
            "tip": "High soil moisture can cause root rot. Check field drainage systems."
        }
    ]

    # ─── Pest Risk Knowledge Base ───────────────────────────────────────────────

    PEST_RISK_RULES = [
        {
            "condition": lambda temp, hum, weather: temp > 30 and hum > 70,
            "level": "Very High",
            "icon": "🐛",
            "color": "very-high",
            "pests": ["Aphids", "Whiteflies", "Spider Mites", "Thrips"],
            "diseases": ["Leaf Blight", "Powdery Mildew", "Rust"],
            "action": "Immediate pest scouting required. Apply preventive pesticides.",
            "prevention": [
                "Spray neem oil solution every 5 days",
                "Install yellow sticky traps",
                "Apply fungicide to prevent blight spread",
                "Increase field inspection frequency to daily"
            ]
        },
        {
            "condition": lambda temp, hum, weather: "Rain" in weather or hum > 80,
            "level": "High",
            "icon": "⚠️",
            "color": "high",
            "pests": ["Caterpillars", "Bollworms", "Stem Borers"],
            "diseases": ["Downy Mildew", "Gray Mold", "Damping Off"],
            "action": "Scout fields regularly. Prepare bio-pesticides.",
            "prevention": [
                "Apply Bacillus thuringiensis (Bt) spray",
                "Remove infected plant parts immediately",
                "Ensure proper spacing for air circulation",
                "Apply copper-based fungicide if rain continues"
            ]
        },
        {
            "condition": lambda temp, hum, weather: temp > 25 and hum > 55,
            "level": "Moderate",
            "icon": "👁️",
            "color": "moderate",
            "pests": ["Leafhoppers", "Mealybugs", "Cutworms"],
            "diseases": ["Leaf Spot", "Anthracnose"],
            "action": "Regular monitoring recommended. Keep records.",
            "prevention": [
                "Inspect crops twice a week",
                "Maintain field hygiene, remove crop residues",
                "Use pheromone traps for early detection",
                "Apply organic pesticide as precaution"
            ]
        },
        {
            "condition": lambda temp, hum, weather: True,  # Default
            "level": "Low",
            "icon": "✅",
            "color": "low",
            "pests": ["Minor soil insects"],
            "diseases": ["Minimal disease risk"],
            "action": "Routine monitoring is sufficient.",
            "prevention": [
                "Weekly field inspection is adequate",
                "Maintain crop rotation practices",
                "Keep records of any unusual observations",
                "Continue standard preventive care"
            ]
        }
    ]

    # ─── Season Knowledge Base ──────────────────────────────────────────────────

    SEASONS = {
        "Kharif": {
            "months": "June – October",
            "crops": ["Rice", "Maize", "Soybean", "Cotton", "Sugarcane"],
            "condition": lambda temp, hum: temp > 25 and hum > 60
        },
        "Rabi": {
            "months": "November – April",
            "crops": ["Wheat", "Barley", "Mustard", "Chickpea", "Peas"],
            "condition": lambda temp, hum: temp < 25 and hum < 60
        },
        "Zaid": {
            "months": "March – June",
            "crops": ["Watermelon", "Cucumber", "Pumpkin", "Moong"],
            "condition": lambda temp, hum: temp > 30 and hum < 55
        }
    }

    def __init__(self, weather_data, soil_moisture, soil_type="loamy", farm_size="medium"):
        self.weather = weather_data
        self.soil_moisture = soil_moisture
        self.soil_type = soil_type.lower()
        self.farm_size = farm_size
        self.temp = weather_data["temperature"]
        self.humidity = weather_data["humidity"]
        self.weather_main = weather_data["weather_main"]

    def _get_climate_zone(self):
        """IR Query Processing: Map weather conditions to climate zone"""
        if self.weather_main in ["Rain", "Drizzle", "Thunderstorm"]:
            return "rainy"
        elif self.temp > 30:
            return "hot_humid" if self.humidity >= 55 else "hot_dry"
        elif self.temp > 18:
            return "mild_humid" if self.humidity >= 55 else "mild_dry"
        else:
            return "cold_humid" if self.humidity >= 55 else "cold_dry"

    def get_crop_advice(self):
        """Retrieve relevant crop recommendations from knowledge base"""
        zone = self._get_climate_zone()
        base = self.CROP_KNOWLEDGE_BASE[zone]
        soil_info = self.SOIL_ADJUSTMENTS.get(self.soil_type, self.SOIL_ADJUSTMENTS["loamy"])

        # Determine recommended season
        recommended_season = None
        for season, info in self.SEASONS.items():
            if info["condition"](self.temp, self.humidity):
                recommended_season = {
                    "name": season,
                    "months": info["months"],
                    "crops": info["crops"]
                }
                break

        return {
            "climate_zone": zone.replace("_", " ").title(),
            "primary_crops": base["primary"],
            "secondary_crops": base["secondary"],
            "avoid_crops": base["avoid"],
            "reason": base["reason"],
            "soil_bonus": soil_info["bonus"],
            "soil_note": soil_info["note"],
            "season": recommended_season
        }

    def get_irrigation_advice(self):
        """Retrieve irrigation recommendations based on moisture & weather"""
        for rule in self.IRRIGATION_RULES:
            if rule["condition"](self.soil_moisture, self.humidity, self.temp):
                return {
                    "level": rule["level"],
                    "icon": rule["icon"],
                    "color": rule["color"],
                    "action": rule["action"],
                    "frequency": rule["frequency"],
                    "amount": rule["amount"],
                    "method": rule["method"],
                    "tip": rule["tip"],
                    "moisture_bar": round(self.soil_moisture)
                }

    def get_pest_risk_advice(self):
        """Retrieve pest risk assessment from knowledge base"""
        for rule in self.PEST_RISK_RULES:
            if rule["condition"](self.temp, self.humidity, self.weather_main):
                return {
                    "level": rule["level"],
                    "icon": rule["icon"],
                    "color": rule["color"],
                    "pests": rule["pests"],
                    "diseases": rule["diseases"],
                    "action": rule["action"],
                    "prevention": rule["prevention"]
                }

    def get_overall_score(self, crop, irrigation, pest):
        """Generate an overall farm health score"""
        score = 100
        # Deduct for irrigation needs
        irrigation_deduct = {"Critical": 40, "High": 25, "Moderate": 15, "Low": 5, "No Irrigation": 0}
        score -= irrigation_deduct.get(irrigation["level"], 10)
        # Deduct for pest risk
        pest_deduct = {"Very High": 30, "High": 20, "Moderate": 10, "Low": 0}
        score -= pest_deduct.get(pest["level"], 5)
        # Bonus for good soil
        if self.soil_type == "loamy":
            score += 5
        score = max(0, min(100, score))

        if score >= 80:
            grade, status = "A", "Excellent"
        elif score >= 65:
            grade, status = "B", "Good"
        elif score >= 50:
            grade, status = "C", "Fair"
        else:
            grade, status = "D", "Needs Attention"

        return {"score": score, "grade": grade, "status": status}

    def generate_full_advisory(self):
        """Main IR retrieval pipeline — generates complete advisory"""
        crop_advice = self.get_crop_advice()
        irrigation_advice = self.get_irrigation_advice()
        pest_advice = self.get_pest_risk_advice()
        score = self.get_overall_score(crop_advice, irrigation_advice, pest_advice)

        return {
            "crop": crop_advice,
            "irrigation": irrigation_advice,
            "pest": pest_advice,
            "score": score,
            "query_params": {
                "soil_moisture": self.soil_moisture,
                "soil_type": self.soil_type,
                "farm_size": self.farm_size
            }
        }
