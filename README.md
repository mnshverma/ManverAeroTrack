# ✈ Manver Aero Track

**Open-source live flight status tracker with departure & arrival weather intelligence.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://manveraerotrack.streamlit.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)

---

## 🌟 Features

- ✈ **Real-time Flight Tracking** — Live ADS-B data via OpenSky Network (no API key needed)
- 🌤 **Temperature & Weather** — Current weather at both departure and arrival airports
- ⇄ **Route Search** — Enter any two IATA airport codes to compare weather instantly
- 🔍 **Airport Search** — Search 180+ airports across India, Middle East, Europe, Asia, Americas & Africa
- 🌡 **Temperature Comparison** — See exactly how much warmer/cooler your destination is
- 📡 **Live Position** — Latitude, longitude, altitude, speed & heading when airborne
- 🎨 **Premium Dark UI** — Glassmorphism design with Orbitron font & smooth animations

---

## 🚀 Quick Start (Local)

```bash
# 1. Clone the repo
git clone https://github.com/your-username/ManverAeroTrack.git
cd ManverAeroTrack

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

Open your browser to **http://localhost:8501**

---

## ☁️ Deploy to Streamlit Community Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **"New app"** → select your repository
4. Set **Main file path**: `app.py`
5. Click **Deploy** — done! 🎉

---

## 📡 Data Sources

| Source | What it provides | Cost |
|--------|-----------------|------|
| [OpenSky Network](https://opensky-network.org) | Live flight positions, ADS-B data | **Free** |
| [Open-Meteo](https://open-meteo.com) | Weather, temperature, wind, visibility | **Free** |
| Built-in Airport DB | 180+ airports with IATA codes & coordinates | **Built-in** |

> ⚠️ **OpenSky Network rate limits**: Anonymous users get ~100 API credits per day. For sustained use, create a free OpenSky account and add credentials.

---

## 🧭 How to Use

### Track a Flight
1. Enter the **flight number** (e.g., `EK202`, `AI101`, `BA249`)
2. Optionally enter departure & arrival IATA codes for better results
3. Click **Track This Flight**

### Route Weather Search
1. Enter **From** airport code (e.g., `DEL`)
2. Enter **To** airport code (e.g., `DXB`)
3. Click **Search Route & Weather** — get full weather comparison instantly

### Airport Search
- Type any city name, airport name, or 3-letter IATA code
- See current temperature and weather conditions

---

## 🗂 Project Structure

```
ManverAeroTrack/
├── app.py              # Main Streamlit application
├── airports.py         # IATA airport database (180+ airports)
├── api_service.py      # OpenSky & Open-Meteo API service layer
├── requirements.txt    # Python dependencies
├── .streamlit/
│   └── config.toml     # Streamlit theme & server config
└── README.md
```

---

## 🛠 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io) with custom CSS (glassmorphism dark theme)
- **Flight Data**: [OpenSky Network REST API](https://opensky-network.org/apidoc/)
- **Weather**: [Open-Meteo API](https://open-meteo.com/en/docs)
- **Language**: Python 3.9+
- **Fonts**: Orbitron + Inter (Google Fonts)

---

## 📋 Supported IATA Airports

**India**: DEL, BOM, BLR, MAA, CCU, HYD, COK, AMD, PNQ, JAI, GOI, LKO, TRV, NAG, and more

**Middle East**: DXB, AUH, DOH, BAH, KWI, MCT, RUH, JED

**Europe**: LHR, CDG, AMS, FRA, MUC, ZRH, MAD, FCO, IST, and 15+ more

**Asia-Pacific**: SIN, KUL, BKK, HKG, NRT, ICN, SYD, MEL, and more

**Americas**: JFK, LAX, ORD, MIA, ATL, YYZ, GRU, MEX, and more

**Africa**: JNB, CAI, NBO, LOS, ADD, CMN

---

## 📜 License

MIT License — free to use, modify, and distribute.

---

## 🙏 Acknowledgements

- [OpenSky Network](https://opensky-network.org) — Community-powered ADS-B flight data
- [Open-Meteo](https://open-meteo.com) — Free open-source weather API
- [Streamlit](https://streamlit.io) — The fastest way to build Python data apps

---

*Built with ❤️ by the Manver team.*
