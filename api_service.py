"""
Manver AeroTrack - API Service Layer
Handles OpenSky Network (flight data) and Open-Meteo (weather) API calls.
"""

import requests
import math
from datetime import datetime, timezone, timedelta

OPENSKY_BASE = "https://opensky-network.org/api"
WEATHER_BASE = "https://api.open-meteo.com/v1"
REQUEST_TIMEOUT = 15

WMO_CODES = {
    0: ("Clear Sky", "☀️"), 1: ("Mainly Clear", "🌤️"), 2: ("Partly Cloudy", "⛅"),
    3: ("Overcast", "☁️"), 45: ("Foggy", "🌫️"), 48: ("Icy Fog", "🌫️"),
    51: ("Light Drizzle", "🌦️"), 53: ("Moderate Drizzle", "🌦️"), 55: ("Heavy Drizzle", "🌧️"),
    61: ("Slight Rain", "🌧️"), 63: ("Moderate Rain", "🌧️"), 65: ("Heavy Rain", "🌧️"),
    71: ("Slight Snow", "🌨️"), 73: ("Moderate Snow", "🌨️"), 75: ("Heavy Snow", "❄️"),
    77: ("Snow Grains", "🌨️"), 80: ("Rain Showers", "🌦️"), 81: ("Moderate Showers", "🌧️"),
    82: ("Violent Showers", "⛈️"), 85: ("Snow Showers", "🌨️"), 86: ("Heavy Snow Showers", "❄️"),
    95: ("Thunderstorm", "⛈️"), 96: ("Thunderstorm + Hail", "⛈️"), 99: ("Severe Thunderstorm", "⛈️"),
}

AIRLINES = {
    "AI": "Air India", "6E": "IndiGo", "SG": "SpiceJet", "UK": "Vistara",
    "IX": "Air India Express", "QP": "Akasa Air", "G8": "Go First",
    "EK": "Emirates", "QR": "Qatar Airways", "EY": "Etihad Airways",
    "FZ": "flydubai", "WY": "Oman Air", "GF": "Gulf Air", "SV": "Saudia",
    "BA": "British Airways", "LH": "Lufthansa", "AF": "Air France",
    "KL": "KLM Royal Dutch", "SK": "Scandinavian Airlines", "IB": "Iberia",
    "AZ": "ITA Airways", "LX": "Swiss International", "OS": "Austrian Airlines",
    "TK": "Turkish Airlines", "SN": "Brussels Airlines",
    "SQ": "Singapore Airlines", "MH": "Malaysia Airlines", "TG": "Thai Airways",
    "GA": "Garuda Indonesia", "PR": "Philippine Airlines", "CX": "Cathay Pacific",
    "CA": "Air China", "MU": "China Eastern", "CZ": "China Southern",
    "NH": "All Nippon Airways", "JL": "Japan Airlines", "KE": "Korean Air",
    "OZ": "Asiana Airlines", "BR": "EVA Air", "CI": "China Airlines",
    "QF": "Qantas", "VA": "Virgin Australia", "NZ": "Air New Zealand",
    "AA": "American Airlines", "UA": "United Airlines", "DL": "Delta Air Lines",
    "WN": "Southwest Airlines", "B6": "JetBlue Airways", "AS": "Alaska Airlines",
    "AC": "Air Canada", "LA": "LATAM Airlines", "ET": "Ethiopian Airlines",
    "SA": "South African Airways", "MS": "EgyptAir", "KQ": "Kenya Airways",
    "AT": "Royal Air Maroc",
}


# ── Math Helpers ──────────────────────────────────────────────────────────────

def haversine_km(lat1, lon1, lat2, lon2) -> float:
    R = 6371
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return round(R * 2 * math.asin(math.sqrt(a)), 0)

def ms_to_kmh(ms): return round(ms * 3.6, 1) if ms else 0.0
def m_to_ft(m): return int(m * 3.28084) if m else 0

def wind_dir_label(deg):
    dirs = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return dirs[int((deg + 11.25) / 22.5) % 16]

def format_visibility(m):
    if m is None: return "N/A"
    return "10+ km" if m >= 10000 else f"{round(m/1000,1)} km"

def format_altitude(m):
    return f"{m_to_ft(m):,} ft" if m else "N/A"

def format_speed(ms):
    return f"{ms_to_kmh(ms):,} km/h" if ms else "N/A"

def get_airline_name(callsign):
    prefix = callsign[:2].upper() if len(callsign) >= 2 else ""
    return AIRLINES.get(prefix, f"Flight {callsign.upper()}")

def great_circle_points(lat1, lon1, lat2, lon2, n=40):
    """Generate n intermediate points along a great-circle arc."""
    points = []
    for i in range(n + 1):
        t = i / n
        lat = lat1 + t * (lat2 - lat1)
        lon = lon1 + t * (lon2 - lon1)
        # Simple curve: add slight arc effect
        mid_offset = math.sin(math.pi * t) * 3
        lat += mid_offset * 0.3
        points.append([lat, lon])
    return points


# ── Flight Data (OpenSky) ─────────────────────────────────────────────────────

def _parse_state(s):
    return {
        "icao24": s[0], "callsign": (s[1] or "").strip(),
        "origin_country": s[2] or "Unknown",
        "longitude": s[5], "latitude": s[6],
        "baro_altitude_m": s[7], "on_ground": s[8],
        "velocity_ms": s[9], "true_track": s[10],
        "vertical_rate": s[11], "geo_altitude_m": s[13],
        "squawk": s[14], "last_contact": s[4],
    }

def fetch_live_flight(callsign: str):
    callsign_clean = callsign.upper().strip().replace(" ", "")
    try:
        resp = requests.get(f"{OPENSKY_BASE}/states/all", timeout=REQUEST_TIMEOUT)
        if resp.status_code != 200:
            return None
        states = resp.json().get("states", []) or []
        matches = [s for s in states if s[1] and callsign_clean in str(s[1]).upper().strip()]
        if not matches:
            return None
        for s in matches:
            if s[8] is False:
                return _parse_state(s)
        return _parse_state(matches[0])
    except Exception:
        return None

def get_flight_info(callsign, dep_airport, arr_airport):
    live = fetch_live_flight(callsign)
    distance_km, est_duration_h, progress_pct, eta_str = None, None, 0, "N/A"

    if dep_airport and arr_airport:
        distance_km = haversine_km(dep_airport["lat"], dep_airport["lon"],
                                    arr_airport["lat"], arr_airport["lon"])
        est_duration_h = round(distance_km / 850, 1)

    if live:
        if dep_airport and arr_airport and live.get("latitude") and live.get("longitude"):
            dist_traveled = haversine_km(dep_airport["lat"], dep_airport["lon"],
                                          live["latitude"], live["longitude"])
            total = haversine_km(dep_airport["lat"], dep_airport["lon"],
                                  arr_airport["lat"], arr_airport["lon"])
            if total > 0:
                progress_pct = min(int((dist_traveled / total) * 100), 99)

        if arr_airport and live.get("latitude") and live.get("velocity_ms"):
            rem = haversine_km(live["latitude"], live["longitude"],
                               arr_airport["lat"], arr_airport["lon"])
            spd = ms_to_kmh(live["velocity_ms"])
            if spd > 0:
                eta_dt = datetime.now(timezone.utc) + timedelta(hours=rem / spd)
                eta_str = eta_dt.strftime("%H:%M UTC")

    status = "On Ground 🛑" if (live and live.get("on_ground")) else ("In Flight ✈️" if live else "Data Unavailable")
    return {
        "callsign": callsign.upper(), "live": live, "status": status,
        "distance_km": distance_km, "est_duration_h": est_duration_h,
        "progress_pct": progress_pct, "eta": eta_str,
        "altitude_m": live.get("baro_altitude_m") if live else None,
        "speed_ms": live.get("velocity_ms") if live else None,
        "on_ground": live.get("on_ground") if live else None,
        "vertical_rate": live.get("vertical_rate") if live else None,
        "heading": live.get("true_track") if live else None,
    }


# ── Weather (Open-Meteo) ──────────────────────────────────────────────────────

def fetch_weather(lat, lon):
    params = {
        "latitude": lat, "longitude": lon,
        "current": [
            "temperature_2m", "apparent_temperature", "relative_humidity_2m",
            "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m",
            "precipitation", "weather_code", "visibility",
            "cloud_cover", "surface_pressure", "uv_index",
            "dew_point_2m",
        ],
        "daily": ["sunrise", "sunset", "uv_index_max", "precipitation_sum",
                  "temperature_2m_max", "temperature_2m_min",
                  "wind_speed_10m_max"],
        "wind_speed_unit": "kmh",
        "timezone": "auto",
        "forecast_days": 1,
    }
    try:
        resp = requests.get(f"{WEATHER_BASE}/forecast", params=params, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        raw = data.get("current", {})
        daily = data.get("daily", {})
        wcode = raw.get("weather_code", 0)
        condition, emoji = WMO_CODES.get(wcode, ("Unknown", "🌡️"))

        sunrise_raw = (daily.get("sunrise") or [None])[0]
        sunset_raw = (daily.get("sunset") or [None])[0]

        def fmt_time(s):
            if not s: return "N/A"
            try: return datetime.fromisoformat(s).strftime("%H:%M")
            except: return "N/A"

        return {
            "temp_c": round(raw.get("temperature_2m", 0), 1),
            "feels_like_c": round(raw.get("apparent_temperature", 0), 1),
            "humidity_pct": raw.get("relative_humidity_2m", 0),
            "wind_kmh": round(raw.get("wind_speed_10m", 0), 1),
            "wind_gusts_kmh": round(raw.get("wind_gusts_10m", 0), 1),
            "wind_dir": raw.get("wind_direction_10m", 0),
            "precipitation_mm": raw.get("precipitation", 0),
            "visibility_m": raw.get("visibility"),
            "cloud_cover_pct": raw.get("cloud_cover", 0),
            "pressure_hpa": round(raw.get("surface_pressure", 0), 1),
            "uv_index": raw.get("uv_index", 0) or 0,
            "dew_point_c": round(raw.get("dew_point_2m", 0), 1),
            "weather_code": wcode, "condition": condition, "emoji": emoji,
            "sunrise": fmt_time(sunrise_raw),
            "sunset": fmt_time(sunset_raw),
            "temp_max": (daily.get("temperature_2m_max") or [None])[0],
            "temp_min": (daily.get("temperature_2m_min") or [None])[0],
            "uv_max": (daily.get("uv_index_max") or [0])[0] or 0,
            "wind_max": (daily.get("wind_speed_10m_max") or [0])[0] or 0,
        }
    except Exception:
        return None


# ── Feature: Carbon Footprint ─────────────────────────────────────────────────

def estimate_carbon(distance_km: float, cabin="Economy") -> dict:
    """Estimate CO₂ per passenger for a flight."""
    # ICAO average emission factors kg CO₂ per km per seat
    factors = {"Economy": 0.255, "Business": 0.510, "First": 0.765}
    factor = factors.get(cabin, 0.255)
    kg = round(distance_km * factor, 1)
    trees = round(kg / 21.7, 1)   # avg tree absorbs 21.7 kg CO₂/yr
    km_drive = round(kg / 0.21)  # ~0.21 kg CO₂/km for avg car
    return {"kg_co2": kg, "trees_equivalent": trees, "km_drive_equivalent": km_drive, "cabin": cabin}


# ── Feature: Packing Suggestions ─────────────────────────────────────────────

def get_packing_suggestions(weather: dict, city: str) -> list[dict]:
    """Return contextual packing suggestions based on destination weather."""
    temp = weather.get("temp_c", 20)
    wind = weather.get("wind_kmh", 0)
    rain = weather.get("precipitation_mm", 0)
    uv = weather.get("uv_index", 0)
    cloud = weather.get("cloud_cover_pct", 0)
    suggestions = []

    # Temperature-based
    if temp < 5:
        suggestions.append({"icon": "🧥", "item": "Heavy Winter Coat", "reason": f"{temp}°C — very cold in {city}"})
        suggestions.append({"icon": "🧤", "item": "Gloves & Scarf", "reason": "Freezing temperatures expected"})
        suggestions.append({"icon": "🥾", "item": "Insulated Boots", "reason": "Cold ground conditions"})
    elif temp < 15:
        suggestions.append({"icon": "🧣", "item": "Light Jacket / Sweater", "reason": f"Cool {temp}°C weather in {city}"})
        suggestions.append({"icon": "👟", "item": "Closed-toe Shoes", "reason": "Mild but cool conditions"})
    elif temp > 35:
        suggestions.append({"icon": "👕", "item": "Light, Breathable Clothing", "reason": f"Very hot {temp}°C in {city}"})
        suggestions.append({"icon": "🧴", "item": "Extra Sunscreen (SPF 50+)", "reason": "Heat + UV exposure"})
        suggestions.append({"icon": "💧", "item": "Hydration Bottle", "reason": "Stay hydrated in extreme heat"})
    elif temp > 28:
        suggestions.append({"icon": "👒", "item": "Sun Hat / Cap", "reason": f"Warm {temp}°C in {city}"})
        suggestions.append({"icon": "😎", "item": "Sunglasses", "reason": "Bright sunny conditions"})

    # Rain-based
    if rain > 0 or "Rain" in weather.get("condition", "") or "Drizzle" in weather.get("condition", ""):
        suggestions.append({"icon": "☂️", "item": "Compact Umbrella", "reason": "Precipitation expected"})
        suggestions.append({"icon": "🥾", "item": "Waterproof Shoes", "reason": "Wet ground conditions"})

    # Wind-based
    if wind > 40:
        suggestions.append({"icon": "🧢", "item": "Secure Hat / Headgear", "reason": f"Windy {wind} km/h conditions"})

    # UV-based
    if uv >= 6:
        suggestions.append({"icon": "🧴", "item": "Sunscreen (SPF 50+)", "reason": f"UV Index {uv:.0f} — high UV exposure"})
        suggestions.append({"icon": "🕶️", "item": "UV-protective Sunglasses", "reason": "High UV radiation"})

    # Snow
    if "Snow" in weather.get("condition", ""):
        suggestions.append({"icon": "❄️", "item": "Snow Boots", "reason": "Snow conditions at destination"})
        suggestions.append({"icon": "🧊", "item": "Anti-slip Grips", "reason": "Icy surfaces likely"})

    # General always-include
    suggestions.append({"icon": "💊", "item": "Travel Medicine Kit", "reason": "Essential for any trip"})
    suggestions.append({"icon": "🔌", "item": "Universal Adapter", "reason": "Check plug types at destination"})
    suggestions.append({"icon": "📱", "item": "Portable Charger", "reason": "Keep devices powered on the go"})

    return suggestions[:8]


# ── Feature: Delay Risk ───────────────────────────────────────────────────────

def assess_delay_risk(dep_weather: dict | None, arr_weather: dict | None) -> dict:
    """Simple heuristic delay risk assessment based on weather."""
    score = 0
    factors = []

    for label, w in [("Departure", dep_weather), ("Arrival", arr_weather)]:
        if not w:
            continue
        wind = w.get("wind_kmh", 0)
        gusts = w.get("wind_gusts_kmh", 0)
        vis_m = w.get("visibility_m") or 10000
        rain = w.get("precipitation_mm", 0)
        cond = w.get("condition", "")

        if wind > 50:
            score += 30; factors.append(f"⚠️ Strong winds at {label} ({wind} km/h)")
        elif wind > 30:
            score += 10; factors.append(f"💨 Moderate winds at {label} ({wind} km/h)")
        if gusts > 70:
            score += 20; factors.append(f"⚠️ Wind gusts {gusts} km/h at {label}")
        if vis_m < 500:
            score += 40; factors.append(f"🌫️ Very low visibility at {label} ({format_visibility(vis_m)})")
        elif vis_m < 2000:
            score += 20; factors.append(f"🌫️ Reduced visibility at {label}")
        if rain > 10:
            score += 20; factors.append(f"🌧️ Heavy rain at {label} ({rain} mm)")
        elif rain > 2:
            score += 10; factors.append(f"🌦️ Light rain at {label}")
        if "Thunder" in cond:
            score += 40; factors.append(f"⛈️ Thunderstorm at {label}")
        if "Snow" in cond:
            score += 30; factors.append(f"❄️ Snow conditions at {label}")

    score = min(score, 100)
    if score >= 60:
        level, color, label_str = "High", "#ff4d4d", "Significant delays possible"
    elif score >= 30:
        level, color, label_str = "Moderate", "#ffb300", "Minor delays possible"
    else:
        level, color, label_str = "Low", "#00e676", "On-time likely"

    return {"score": score, "level": level, "color": color,
            "label": label_str, "factors": factors}


# ── Feature: UV Safety ────────────────────────────────────────────────────────

def uv_category(uv: float) -> tuple[str, str]:
    if uv < 3: return "Low", "🟢"
    if uv < 6: return "Moderate", "🟡"
    if uv < 8: return "High", "🟠"
    if uv < 11: return "Very High", "🔴"
    return "Extreme", "🟣"
