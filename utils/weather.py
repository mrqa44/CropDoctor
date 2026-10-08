import requests

def get_spraying_weather(lat=30.3753, lon=69.3451):
    """
    Fetches real-time weather from Open-Meteo (Free, NO API key needed).
    Calculates if it is safe for farmers to spray treatments.
    Defaults to central Pakistan coordinates.
    """
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=precipitation_probability_max&timezone=auto"
        resp = requests.get(url, timeout=5).json()
        
        current = resp.get("current_weather", {})
        wind_speed = current.get("windspeed", 0)
        temp = current.get("temperature", 0)
        rain_prob = resp.get("daily", {}).get("precipitation_probability_max", [0])[0]
        
        advice = []
        is_good_to_spray = True
        
        if wind_speed > 15:
            advice.append("⚠️ High wind speed. Spraying not recommended (chemicals drift).")
            is_good_to_spray = False
        if temp > 30:
            advice.append("⚠️ High temperature. Spray early morning or late evening.")
        if rain_prob > 40:
            advice.append(f"🌧️ {rain_prob}% chance of rain today. Treatments may wash away.")
            is_good_to_spray = False
            
        if is_good_to_spray:
            advice.append("✅ Weather is optimal for applying treatments today.")
            
        return {"temp": temp, "wind": wind_speed, "advice": advice}
    except Exception as e:
        print(f"Weather API Error: {e}")
        return None
