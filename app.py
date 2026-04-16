"""
Manver Aero Track — Premium Live Flight & Weather Intelligence
Fixing crash points and improving robustness.
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
)

# ─── Data Prep ────────────────────────────────────────────────────────────────
# Enhanced searchability: City - Code - Country
AIRPORT_OPTIONS = [f"{info['city']} ({code}) — {info['country']}" for code, info in AIRPORTS.items()]
AIRPORT_OPTIONS.sort()

def extract_iata(option_str):
    if not option_str: return None
    try:
        # Extract 3-letter code inside parentheses
        start = option_str.find("(") + 1
        end = option_str.find(")")
        return option_str[start:end].upper()
    except: return None

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Orbitron:wght@400;700;900&display=swap');

:root {
    --bg-primary: #060b1a;
    --accent-cyan: #00d4ff;
    --text-primary: #f0f4ff;
    --border: rgba(255,255,255,0.08);
}

.stApp { background-color: var(--bg-primary) !important; color: var(--text-primary); }

.mat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid var(--border);
}

.mat-logo {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 22px;
    font-weight: 800;
    background: linear-gradient(135deg, #00d4ff, #7b5ea7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.glass-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 15px;
    backdrop-filter: blur(10px);
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
    gap: 12px;
}

.metric-box {
    background: rgba(255,255,255,0.02);
    border: 1px solid var(--border);
    padding: 12px;
    border-radius: 10px;
    text-align: center;
}

.m-val { font-family: 'Orbitron', sans-serif; font-size: 16px; font-weight: 700; }
.m-lbl { font-size: 9px; color: #8899bb; text-transform: uppercase; margin-top: 2px; }

/* Responsive adjustments */
@media (max-width: 768px) {
    .hero-title { font-size: 2rem !important; }
}

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="mat-header">
    <div class="mat-logo">MANVER AERO TRACK</div>
    <div style="color: #00e676; font-size: 11px; font-weight: 700;">● SYSTEM ONLINE</div>
</div>
""", unsafe_allow_html=True)

# ─── Search Section ───────────────────────────────────────────────────────────
with st.container():
    c_search, c_stats = st.columns([3, 1])
    
    with c_search:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        s_mode = st.radio("Intelligence Type", ["Live Flight Tracker", "Route Diagnostics"], horizontal=True, label_visibility="collapsed")
        
        if s_mode == "Live Flight Tracker":
            f_num = st.text_input("FLIGHT NUMBER", placeholder="e.g. EK202")
            o1, o2 = st.columns(2)
            with o1:
                dep_opt = st.selectbox("ORIGIN", ["Select Airport..."] + AIRPORT_OPTIONS)
            with o2:
                arr_opt = st.selectbox("DESTINATION", ["Select Airport..."] + AIRPORT_OPTIONS)
            go_btn = st.button("INITIATE TRACKING", use_container_width=True)
        else:
            o1, o2 = st.columns(2)
            with o1: r_f = st.selectbox("FROM", AIRPORT_OPTIONS)
            with o2: r_t = st.selectbox("TO", AIRPORT_OPTIONS)
            go_btn = st.button("SYNC ROUTE", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c_stats:
        st.markdown("""
        <div class="glass-card" style="height: 100%;">
            <div style="font-size: 10px; color: #8899bb; font-weight: 700;">AIRSPACE LOAD</div>
            <div style="font-size: 22px; font-weight: 800; color: #00d4ff;">89%</div>
            <div style="font-size: 9px; color: #556688; margin-top: 10px;">High traffic protocols active. Monitoring 18k+ active transponders.</div>
        </div>
        """, unsafe_allow_html=True)

# ─── Data Execution ───────────────────────────────────────────────────────────
if go_btn:
    with st.spinner("Processing satellite telemetry..."):
        try:
            if s_mode == "Live Flight Tracker":
                callsign = f_num.strip().upper() if f_num else "UNKNOWN"
                d_iata = extract_iata(dep_opt) if "Select" not in dep_opt else None
                a_iata = extract_iata(arr_opt) if "Select" not in arr_opt else None
                
                dep_ap = get_airport(d_iata) if d_iata else None
                arr_ap = get_airport(a_iata) if a_iata else None
                
                # Fetch all data once to avoid repeated API calls
                flight = get_flight_info(callsign, dep_ap, arr_ap)
                dep_w = fetch_weather(dep_ap['lat'], dep_ap['lon']) if dep_ap else None
                arr_w = fetch_weather(arr_ap['lat'], arr_ap['lon']) if arr_ap else None
                
                # Header Card
                st.markdown(f"""
                <div class="glass-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 10px; color: #8899bb; font-weight: 700;">FLIGHT ID</div>
                            <div style="font-family: Orbitron; font-size: 28px; font-weight: 900; color: #00d4ff;">{callsign}</div>
                            <div style="font-size: 13px; color: #fff;">{get_airline_name(callsign)}</div>
                        </div>
                        <div style="text-align: right;">
                            <span style="font-size: 10px; font-weight: 700; color: #00e676;">{flight.get('status', 'Unknown').upper()}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Map & Metrics
                m_col, d_col = st.columns([3, 2])
                
                with m_col:
                    st.markdown('<div class="glass-card" style="padding: 10px;">', unsafe_allow_html=True)
                    m_lat, m_lon, zoom = 20, 0, 2
                    if flight.get('live') and flight['live'].get('latitude'):
                        m_lat, m_lon, zoom = flight['live']['latitude'], flight['live']['longitude'], 4
                    elif dep_ap:
                        m_lat, m_lon, zoom = dep_ap['lat'], dep_ap['lon'], 3
                    
                    m = folium.Map(location=[m_lat, m_lon], zoom_start=zoom, tiles="cartodbdark_matter")
                    if dep_ap and arr_ap:
                        p = great_circle_points(dep_ap['lat'], dep_ap['lon'], arr_ap['lat'], arr_ap['lon'])
                        folium.PolyLine(p, color="#7b5ea7", weight=2, opacity=0.4).add_to(m)
                    if flight.get('live') and flight['live'].get('latitude'):
                        folium.Marker([m_lat, m_lon], icon=folium.Icon(color='red', icon='plane', prefix='fa')).add_to(m)
                    
                    st_folium(m, width="100%", height=300, key="radar_map")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                with d_col:
                    st.markdown(f"""
                    <div class="metric-grid">
                        <div class="metric-box"><div class="m-val">{format_altitude(flight.get('altitude_m'))}</div><div class="m-lbl">Altitude</div></div>
                        <div class="metric-box"><div class="m-val">{format_speed(flight.get('speed_ms'))}</div><div class="m-lbl">Speed</div></div>
                        <div class="metric-box"><div class="m-val">{flight.get('eta', 'N/A')}</div><div class="m-lbl">ETA (UTC)</div></div>
                        <div class="metric-box"><div class="m-val">{f"{int(flight['distance_km']):,} km" if flight.get('distance_km') else 'N/A'}</div><div class="m-lbl">Distance</div></div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Destination Insight
                    if arr_ap and arr_w:
                        st.markdown(f"""
                        <div class="glass-card" style="margin-top: 15px;">
                            <div style="font-size: 10px; color: #8899bb; font-weight: 700;">DESTINATION: {arr_ap['city']}</div>
                            <div style="display: flex; align-items: center; gap: 12px; margin-top: 8px;">
                                <div style="font-size: 28px;">{arr_w['emoji']}</div>
                                <div style="font-size: 24px; font-weight: 800;">{arr_w['temp_c']}°C</div>
                            </div>
                            <div style="font-size: 11px; color: #8899bb; margin-top: 4px;">{arr_w['condition']} · Visibility {format_visibility(arr_w.get('visibility_m'))}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info("Additional destination data unavailable.")

                # Intelligence Tabs
                st.markdown("<br>", unsafe_allow_html=True)
                i1, i2, i3 = st.tabs(["🛡️ SAFETY", "🌱 ECO", "🎒 PACKING"])
                
                with i1:
                    risk = assess_delay_risk(dep_w, arr_w)
                    st.markdown(f"""
                    <div style="display: flex; flex-wrap: wrap; gap: 15px;">
                        <div class="glass-card" style="flex: 1; border-left: 4px solid {risk['color']};">
                            <h5 style="margin: 0; color: {risk['color']};">DELAY RISK: {risk['level'].upper()}</h5>
                            <p style="font-size: 12px; color: #8899bb; margin-top: 5px;">{risk['label']}</p>
                        </div>
                        <div class="glass-card" style="flex: 1;">
                            <div style="font-size: 9px; color: #8899bb;">UV INDEX</div>
                            <div style="font-size: 18px; font-weight: 700;">{arr_w.get('uv_index', 'N/A') if arr_w else 'N/A'}</div>
                            <div style="font-size: 10px; color: #ffb300;">{uv_category(arr_w.get('uv_index') or 0)[0] if arr_w else ''}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with i2:
                    if flight.get('distance_km'):
                        eco = estimate_carbon(flight['distance_km'])
                        st.markdown(f'<div class="glass-card" style="text-align: center;"><div style="font-size: 22px; font-weight: 800; color: #00e676;">{eco["kg_co2"]} kg</div><div style="font-size: 10px; color: #8899bb;">ESTIMATED CO₂ EMISSION</div></div>', unsafe_allow_html=True)
                
                with i3:
                    if arr_ap and arr_w:
                        packs = get_packing_suggestions(arr_w, arr_ap['city'])
                        if packs:
                            cols = st.columns(min(len(packs), 4))
                            for idx, p in enumerate(packs):
                                cols[idx % 4].markdown(f'<div class="glass-card" style="padding: 10px; text-align: center;"><div style="font-size: 20px;">{p["icon"]}</div><div style="font-weight: 700; font-size: 11px; margin-top: 3px;">{p["item"]}</div></div>', unsafe_allow_html=True)
                        else:
                            st.info("No specific packing items suggested for this climate.")

            elif s_mode == "Route Diagnostics":
                st.info("Route Diagnostics synchronized. Analyzing data...")

        except Exception as e:
            st.error(f"⚠️ Intelligence Interrupted: {str(e)}")
            st.info("Our satellite link encountered an anomaly. Please verify the flight ID and airport codes and try again.")

else:
    # Landing State
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0;">
        <h1 style="font-family: 'Orbitron'; font-size: 2.5rem; margin-bottom: 0.5rem;">The Sky is Your Database</h1>
        <p style="color: #8899bb; max-width: 500px; margin: 0 auto;">Premium open-source flight intelligence powered by real-time ADS-B and meteorological data feeds.</p>
    </div>
    """, unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; color: #445577; font-size: 10px; padding: 20px 0; border-top: 1px solid var(--border); margin-top: 40px;">
    MANVER AERO TRACK · PREMIUM SUITE · v1.2.1 Stable
</div>
""", unsafe_allow_html=True)
