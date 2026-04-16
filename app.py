"""
Manver Aero Track — Premium Live Flight & Weather Intelligence
Refined, responsive, and minimalist suite.
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import time
from datetime import datetime, timezone

from airports import AIRPORTS, get_airport, search_airports
from api_service import (
    get_flight_info, fetch_weather, get_airline_name,
    wind_dir_label, format_visibility, format_altitude, format_speed,
    estimate_carbon, get_packing_suggestions, assess_delay_risk, uv_category,
    great_circle_points
)

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Manver Aero Track",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Data Prep ────────────────────────────────────────────────────────────────
# Create a list of "City (IATA) - Airport" for the selectboxes
AIRPORT_OPTIONS = [f"{info['city']} ({code}) — {info['name']}" for code, info in AIRPORTS.items()]
AIRPORT_OPTIONS.sort()

def extract_iata(option_str):
    if not option_str: return None
    try: return option_str.split("(")[1].split(")")[0]
    except: return None

# ─── Custom CSS (Responsive & Minimalist) ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Orbitron:wght@400;700;900&display=swap');

:root {
    --bg-primary: #060b1a;
    --accent-cyan: #00d4ff;
    --accent-violet: #7b5ea7;
    --text-primary: #f0f4ff;
    --border: rgba(255,255,255,0.08);
}

/* Global Styles */
.stApp {
    background: radial-gradient(circle at 10% 10%, rgba(0,212,255,0.05) 0%, transparent 40%),
                var(--bg-primary) !important;
}

/* Responsive Container */
.main-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

/* Header */
.mat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 0;
    margin-bottom: 2rem;
    border-bottom: 1px solid var(--border);
}

.mat-logo {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 20px;
    font-weight: 800;
    letter-spacing: 0.1em;
    background: linear-gradient(135deg, #00d4ff, #7b5ea7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Premium Card */
.glass-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    backdrop-filter: blur(10px);
}

/* Metrics Row - Responsive Grid */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 15px;
    margin: 20px 0;
}

.metric-item {
    background: rgba(255,255,255,0.02);
    border: 1px solid var(--border);
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}

.metric-val { font-family: 'Orbitron', sans-serif; font-size: 18px; font-weight: 700; color: #fff; }
.metric-lbl { font-size: 10px; color: #8899bb; text-transform: uppercase; margin-top: 4px; }

/* Status Badges */
.badge {
    font-size: 11px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 6px;
    text-transform: uppercase;
}
.badge-live { background: rgba(0,230,118,0.1); color: #00e676; border: 1px solid rgba(0,230,118,0.2); }

/* Responsive adjustments for mobile */
@media (max-width: 768px) {
    .mat-header { flex-direction: column; gap: 10px; text-align: center; }
    .hero-title { font-size: 2rem !important; }
}

/* Hide Unwanted UI */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── Navigation Header ────────────────────────────────────────────────────────
st.markdown("""
<div class="main-content">
    <div class="mat-header">
        <div class="mat-logo">MANVER AERO TRACK</div>
        <div class="badge badge-live">● SATELLITE SYNC ACTIVE</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Dashboard Search ─────────────────────────────────────────────────────────
with st.container():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    col_input, col_info = st.columns([2, 1])
    
    with col_input:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        search_type = st.radio("Search Intelligence", ["Flight Tracker", "Route Sync"], horizontal=True, label_visibility="collapsed")
        
        if search_type == "Flight Tracker":
            f_code = st.text_input("ENTER FLIGHT NUMBER", placeholder="e.g. EK202, AI101")
            c1, c2 = st.columns(2)
            with c1:
                dep_sel = st.selectbox("FROM (CITY/IATA)", [""] + AIRPORT_OPTIONS, key="dep_sel", help="Search and select departure airport")
            with c2:
                arr_sel = st.selectbox("TO (CITY/IATA)", [""] + AIRPORT_OPTIONS, key="arr_sel", help="Search and select destination airport")
            
            trigger_btn = st.button("TRACK NOW", use_container_width=True)
            
        else:
            c1, c2 = st.columns(2)
            with c1:
                r_from = st.selectbox("FROM", AIRPORT_OPTIONS, key="r_from")
            with c2:
                r_to = st.selectbox("TO", AIRPORT_OPTIONS, key="r_to")
            trigger_btn = st.button("SYNC ROUTE", use_container_width=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

    with col_info:
        st.markdown(f"""
        <div class="glass-card" style="height: 100%;">
            <div style="font-size: 12px; color: #8899bb; font-weight: 700; margin-bottom: 10px;">GLOBAL STATS</div>
            <div style="font-size: 24px; font-weight: 800; color: #00d4ff;">18,492</div>
            <div style="font-size: 10px; color: #556688; margin-bottom: 15px;">AIRCRAFT IN AIRSPACE</div>
            <hr style="opacity: 0.1;">
            <div style="font-size: 12px; font-weight: 600; color: #fff;">Manver Premium Suite</div>
            <div style="font-size: 11px; color: #8899bb;">High-frequency ADS-B tracking enabled via community receivers.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ─── Results Handling ─────────────────────────────────────────────────────────
if trigger_btn:
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    with st.spinner("Locking on Signal..."):
        if search_type == "Flight Tracker":
            callsign = f_code.strip().upper() if f_code else "UNKNOWN"
            d_iata = extract_iata(dep_sel)
            a_iata = extract_iata(arr_sel)
            
            dep_ap = get_airport(d_iata) if d_iata else None
            arr_ap = get_airport(a_iata) if a_iata else None
            
            flight = get_flight_info(callsign, dep_ap, arr_ap)
            
            # 1. Mission Header
            st.markdown(f"""
            <div class="glass-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-end;">
                    <div>
                        <div style="font-size: 10px; color: #8899bb; font-weight: 700;">FLIGHT RADAR CALLSIGN</div>
                        <div style="font-family: Orbitron; font-size: 32px; font-weight: 900; color: #00d4ff;">{callsign}</div>
                        <div style="color: #fff; font-size: 14px;">{get_airline_name(callsign)}</div>
                    </div>
                    <div style="text-align: right;">
                        <span class="badge badge-live">{flight['status']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 2. Map & Telemetry
            col_map, col_tele = st.columns([3, 2])
            
            with col_map:
                st.markdown('<div class="glass-card" style="padding: 10px;">', unsafe_allow_html=True)
                m_lat, m_lon = 20, 0
                zoom = 2
                if flight['live'] and flight['live']['latitude']:
                    m_lat, m_lon = flight['live']['latitude'], flight['live']['longitude']
                    zoom = 4
                elif dep_ap:
                    m_lat, m_lon = dep_ap['lat'], dep_ap['lon']
                    zoom = 3
                
                m = folium.Map(location=[m_lat, m_lon], zoom_start=zoom, tiles="cartodbdark_matter")
                if dep_ap and arr_ap:
                    path = great_circle_points(dep_ap['lat'], dep_ap['lon'], arr_ap['lat'], arr_ap['lon'])
                    folium.PolyLine(path, color="#7b5ea7", weight=2, opacity=0.5).add_to(m)
                
                if flight['live'] and flight['live']['latitude']:
                    folium.Marker([flight['live']['latitude'], flight['live']['longitude']], icon=folium.Icon(color='red', icon='plane', prefix='fa')).add_to(m)
                
                st_folium(m, width="100%", height=350, key="main_map")
                st.markdown('</div>', unsafe_allow_html=True)
                
            with col_tele:
                st.markdown(f"""
                <div class="metrics-grid" style="grid-template-columns: 1fr 1fr;">
                    <div class="metric-item">
                        <div class="metric-val">{format_altitude(flight['altitude_m'])}</div>
                        <div class="metric-lbl">Altitude</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-val">{format_speed(flight['speed_ms'])}</div>
                        <div class="metric-lbl">Speed</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-val">{flight['eta']}</div>
                        <div class="metric-lbl">ETA (UTC)</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-val">{f"{int(flight['distance_km']):,} km" if flight['distance_km'] else 'N/A'}</div>
                        <div class="metric-lbl">Distance</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Weather Preview
                if arr_ap:
                    w = fetch_weather(arr_ap['lat'], arr_ap['lon'])
                    if w:
                        st.markdown(f"""
                        <div class="glass-card" style="margin-top: 5px;">
                            <div style="font-size: 10px; color: #8899bb; font-weight: 700;">DESTINATION: {arr_ap['city']}</div>
                            <div style="display: flex; align-items: center; gap: 15px; margin-top: 10px;">
                                <div style="font-size: 32px;">{w['emoji']}</div>
                                <div style="font-size: 28px; font-weight: 800; color: #fff;">{w['temp_c']}°C</div>
                            </div>
                            <div style="font-size: 12px; color: #8899bb; margin-top: 5px;">{w['condition']} · Feels like {w['feels_like_c']}°C</div>
                        </div>
                        """, unsafe_allow_html=True)
            
            # 3. Expanded Intelligence Tabs
            st.markdown("<br>", unsafe_allow_html=True)
            t1, t2, t3 = st.tabs(["🛡️ FLIGHT SECURITY", "🌱 SUSTAINABILITY", "🎒 PACKING GUIDES"])
            
            with t1:
                risk = assess_delay_risk(fetch_weather(dep_ap['lat'], dep_ap['lon']) if dep_ap else None, 
                                          fetch_weather(arr_ap['lat'], arr_ap['lon']) if arr_ap else None)
                st.markdown(f"""
                <div style="display: flex; flex-wrap: wrap; gap: 20px;">
                    <div class="glass-card" style="flex: 1; min-width: 280px; border-left: 4px solid {risk['color']};">
                        <h4 style="margin: 0; color: {risk['color']};">DELAY RISK: {risk['level'].upper()}</h4>
                        <p style="font-size: 14px; color: #8899bb;">{risk['label']}</p>
                    </div>
                    <div class="glass-card" style="flex: 1; min-width: 200px;">
                        <div style="font-size: 10px; color: #8899bb;">DESTINATION UV</div>
                        <div style="font-size: 24px; font-weight: 800;">{fetch_weather(arr_ap['lat'], arr_ap['lon'])['uv_index'] if arr_ap else 'N/A'}</div>
                        <div style="font-size: 11px; color: #ffb300;">{uv_category(fetch_weather(arr_ap['lat'], arr_ap['lon'])['uv_index'])[0] if arr_ap else ''}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with t2:
                if flight['distance_km']:
                    carbon = estimate_carbon(flight['distance_km'])
                    st.markdown(f"""
                    <div class="glass-card" style="text-align: center;">
                        <h4 style="color: #00e676;">Environmental Footprint</h4>
                        <div class="metrics-grid">
                            <div class="metric-item"><div class="metric-val">{carbon['kg_co2']} kg</div><div class="metric-lbl">Total CO₂</div></div>
                            <div class="metric-item"><div class="metric-val">{carbon['trees_equivalent']}</div><div class="metric-lbl">Trees to offset</div></div>
                            <div class="metric-item"><div class="metric-val">{carbon['km_drive_equivalent']} km</div><div class="metric-lbl">Road trip equivalent</div></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with t3:
                if arr_ap:
                    w = fetch_weather(arr_ap['lat'], arr_ap['lon'])
                    packs = get_packing_suggestions(w, arr_ap['city'])
                    cols = st.columns(min(len(packs), 4))
                    for idx, p in enumerate(packs):
                        cols[idx % 4].markdown(f"""
                        <div class="glass-card" style="padding: 10px; text-align: center;">
                            <div style="font-size: 24px;">{p['icon']}</div>
                            <div style="font-weight: 700; font-size: 12px; margin-top: 5px;">{p['item']}</div>
                            <div style="font-size: 9px; color: #8899bb;">{p['reason']}</div>
                        </div>
                        """, unsafe_allow_html=True)
        
        elif search_type == "Route Sync":
            from_iata = extract_iata(r_from)
            to_iata = extract_iata(r_to)
            dep_ap = get_airport(from_iata)
            arr_ap = get_airport(to_iata)
            
            if dep_ap and arr_ap:
                st.markdown(f'<h4 style="font-family: Orbitron; text-align: center;">{dep_ap["city"]} → {arr_ap["city"]}</h4>', unsafe_allow_html=True)
                # Map
                m = folium.Map(location=[(dep_ap['lat']+arr_ap['lat'])/2, (dep_ap['lon']+arr_ap['lon'])/2], zoom_start=3, tiles="cartodbdark_matter")
                path = great_circle_points(dep_ap['lat'], dep_ap['lon'], arr_ap['lat'], arr_ap['lon'])
                folium.PolyLine(path, color="#00d4ff", weight=3, opacity=0.8).add_to(m)
                st_folium(m, width="100%", height=400, key="route_map")
                
                # Weather comparison logic here...
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Landing State
    st.markdown("""
    <div class="main-content">
        <div style="text-align: center; padding: 4rem 0;">
            <h1 class="hero-title" style="font-size: 3rem; margin-bottom: 1rem;">Seamless Flight Intelligence</h1>
            <p style="color: #8899bb; font-size: 1.1rem; max-width: 600px; margin: 0 auto;">
                Manver Aero Track combining premium aesthetics with real-time ADS-B satellite data. 
                Search by flight number or sync routes to begin.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── Global Footer ────────────────────────────────────────────────────────────
st.markdown("""
<br><br>
<div style="text-align: center; color: #445577; font-size: 11px; padding: 20px 0; border-top: 1px solid var(--border);">
    MANVER AERO TRACK · PREMIUM SUITE · OPEN SOURCE<br>
    Built with Folium, OpenSky & Open-Meteo REST APIs.
</div>
""", unsafe_allow_html=True)
