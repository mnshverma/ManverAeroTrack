"""
Manver Aero Track — Premium Live Flight & Weather Intelligence
An open-source, high-performance tracking suite.
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import time
from datetime import datetime, timezone

from airports import get_airport, search_airports
from api_service import (
    get_flight_info, fetch_weather, get_airline_name,
    wind_dir_label, format_visibility, format_altitude, format_speed,
    estimate_carbon, get_packing_suggestions, assess_delay_risk, uv_category,
    great_circle_points
)

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Manver Aero Track — Live Flight Tracker",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS (Premium Glassmorphism) ───────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Orbitron:wght@400;700;900&display=swap');

:root {
    --bg-primary: #060b1a;
    --bg-card: rgba(255,255,255,0.04);
    --accent-cyan: #00d4ff;
    --accent-violet: #7b5ea7;
    --text-primary: #f0f4ff;
    --text-secondary: #8899bb;
    --border: rgba(255,255,255,0.08);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

.stApp {
    background: radial-gradient(circle at 20% 10%, rgba(0,212,255,0.08) 0%, transparent 40%),
                radial-gradient(circle at 80% 80%, rgba(123,94,167,0.08) 0%, transparent 40%),
                var(--bg-primary) !important;
}

/* Header & Brand */
.mat-header {
    background: rgba(6,11,26,0.8);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--border);
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 1000;
}
.mat-brand-name {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 24px;
    font-weight: 900;
    background: linear-gradient(135deg, #00d4ff, #7b5ea7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 0.05em;
}

/* Glass Cards */
.glass-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 24px;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    transition: all 0.3s ease;
}
.glass-card:hover { border-color: rgba(0,212,255,0.3); }

/* Typography */
.hero-title {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 3.5rem;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(to right, #fff, #8899bb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-top: 2rem;
}
.hero-subtitle {
    text-align: center;
    color: var(--text-secondary);
    font-size: 1.1rem;
    max-width: 600px;
    margin: 1rem auto 3rem;
}

/* Tabs & Inputs */
.stTabs [data-baseweb="tab-list"] { background: transparent; border-bottom: 2px solid var(--border); }
.stTabs [data-baseweb="tab"] { color: var(--text-secondary) !important; font-weight: 600; }
.stTabs [aria-selected="true"] { color: var(--accent-cyan) !important; border-bottom-color: var(--accent-cyan) !important; }

/* Status Badges */
.status-pill {
    padding: 4px 12px;
    border-radius: 99px;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
}
.status-live { background: rgba(0,230,118,0.15); color: #00e676; border: 1px solid rgba(0,230,118,0.3); }
.status-ground { background: rgba(255,179,0,0.15); color: #ffb300; border: 1px solid rgba(255,179,0,0.3); }

/* Hide Streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── Navigation & Header ──────────────────────────────────────────────────────
st.markdown("""
<div class="mat-header">
    <div class="mat-brand-name">MANVER AERO TRACK</div>
    <div style="display: flex; gap: 20px; align-items: center;">
        <span style="color: #00e676; font-size: 14px; font-weight: 600;">● LIVE AIRSPACE</span>
        <button style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: white; padding: 6px 12px; border-radius: 8px; cursor: pointer;">Open Source</button>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Hero Section ─────────────────────────────────────────────────────────────
st.markdown('<h1 class="hero-title">Elevate Your Journey</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Real-time flight intelligence, environmental insights, and destination intelligence in one premium interface.</p>', unsafe_allow_html=True)

# ─── Main Interface ───────────────────────────────────────────────────────────
col_l, col_r = st.columns([2, 5])

with col_l:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Tracking Command")
    
    track_mode = st.radio("Mode", ["Flight Number", "Route Search", "Airport Intelligence"], horizontal=True, label_visibility="collapsed")
    
    if track_mode == "Flight Number":
        flight_id = st.text_input("FLIGHT NUMBER", placeholder="e.g. EK202, SQ308", help="IATA code + Number")
        dep_iata = st.text_input("DEPARTURE (OPTIONAL)", placeholder="DEL, LHR")
        arr_iata = st.text_input("ARRIVAL (OPTIONAL)", placeholder="DXB, SIN")
        track_btn = st.button("TRACK FLIGHT", use_container_width=True)
    
    elif track_mode == "Route Search":
        from_iata = st.text_input("FROM (IATA)", placeholder="BOM")
        to_iata = st.text_input("TO (IATA)", placeholder="JFK")
        track_btn = st.button("ANALYZE ROUTE", use_container_width=True)
        
    else:
        ap_query = st.text_input("SEARCH AIRPORT", placeholder="Mumbai or DEL")
        track_btn = st.button("SEARCH INTELLIGENCE", use_container_width=True)
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent Features / Info
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("🌍 Sustainability Info", expanded=False):
        st.write("Manver Aero Track calculates carbon footprint for every flight using ICAO average emission factors.")
    with st.expander("🛡️ Data Sovereignty", expanded=False):
        st.write("This application is 100% Open Source. We use public APIs from OpenSky Network and Open-Meteo.")

# ─── Results Handling ─────────────────────────────────────────────────────────
with col_r:
    if 'track_btn' in locals() and track_btn:
        if track_mode == "Flight Number" and flight_id:
            with st.spinner("Synchronizing with Satellite Data..."):
                callsign = flight_id.strip().upper()
                dep_ap = get_airport(dep_iata.strip().upper()) if dep_iata else None
                arr_ap = get_airport(arr_iata.strip().upper()) if arr_iata else None
                
                flight = get_flight_info(callsign, dep_ap, arr_ap)
                
                # Layout for Flight Result
                st.markdown(f"""
                <div class="glass-card" style="margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="color: var(--text-secondary); font-size: 12px; font-weight: 700;">LIVE CALLSIGN</span>
                            <div style="font-family: Orbitron; font-size: 32px; font-weight: 900; color: var(--accent-cyan);">{callsign}</div>
                            <div style="color: #fff; font-weight: 600;">{get_airline_name(callsign)}</div>
                        </div>
                        <div class="status-pill {'status-live' if 'Live' in flight['status'] or 'Flight' in flight['status'] else 'status-ground'}">
                            {flight['status']}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Map Section
                st.markdown('<div class="glass-card" style="padding: 10px; margin-bottom: 20px;">', unsafe_allow_html=True)
                
                # Initialize Map
                m_lat, m_lon = 20, 0
                zoom = 2
                
                if flight['live'] and flight['live']['latitude']:
                    m_lat, m_lon = flight['live']['latitude'], flight['live']['longitude']
                    zoom = 4
                elif dep_ap:
                    m_lat, m_lon = dep_ap['lat'], dep_ap['lon']
                    zoom = 4
                
                m = folium.Map(location=[m_lat, m_lon], zoom_start=zoom, tiles="cartodbdark_matter")
                
                # Add route path if airports known
                if dep_ap and arr_ap:
                    path = great_circle_points(dep_ap['lat'], dep_ap['lon'], arr_ap['lat'], arr_ap['lon'])
                    folium.PolyLine(path, color="#7b5ea7", weight=2, opacity=0.6, dash_array="10, 10").add_to(m)
                    folium.Marker([dep_ap['lat'], dep_ap['lon']], tooltip=dep_ap['iata'], icon=folium.Icon(color='blue', icon='plane-departure', prefix='fa')).add_to(m)
                    folium.Marker([arr_ap['lat'], arr_ap['lon']], tooltip=arr_ap['iata'], icon=folium.Icon(color='purple', icon='plane-arrival', prefix='fa')).add_to(m)
                
                # Add current position
                if flight['live'] and flight['live']['latitude']:
                    folium.Marker(
                        [flight['live']['latitude'], flight['live']['longitude']],
                        popup=f"{callsign}",
                        icon=folium.Icon(color='red', icon='plane', prefix='fa')
                    ).add_to(m)
                
                st_folium(m, width="100%", height=400)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Technical Insights Row
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.markdown(f'<div class="glass-card" style="text-align: center;"><div style="color: var(--text-secondary); font-size: 10px;">ALTITUDE</div><div style="font-size: 18px; font-weight: 800; color: #fff;">{format_altitude(flight["altitude_m"])}</div></div>', unsafe_allow_html=True)
                with c2:
                    st.markdown(f'<div class="glass-card" style="text-align: center;"><div style="color: var(--text-secondary); font-size: 10px;">SPEED</div><div style="font-size: 18px; font-weight: 800; color: #fff;">{format_speed(flight["speed_ms"])}</div></div>', unsafe_allow_html=True)
                with c3:
                    st.markdown(f'<div class="glass-card" style="text-align: center;"><div style="color: var(--text-secondary); font-size: 10px;">ETA (UTC)</div><div style="font-size: 18px; font-weight: 800; color: #fff;">{flight["eta"]}</div></div>', unsafe_allow_html=True)
                with c4:
                    dist = f"{int(flight['distance_km']):,} km" if flight['distance_km'] else "N/A"
                    st.markdown(f'<div class="glass-card" style="text-align: center;"><div style="color: var(--text-secondary); font-size: 10px;">DISTANCE</div><div style="font-size: 18px; font-weight: 800; color: #fff;">{dist}</div></div>', unsafe_allow_html=True)
                
                # Weather & Intelligence
                st.markdown("<br>", unsafe_allow_html=True)
                wc_l, wc_r = st.columns(2)
                
                dep_w = fetch_weather(dep_ap['lat'], dep_ap['lon']) if dep_ap else None
                arr_w = fetch_weather(arr_ap['lat'], arr_ap['lon']) if arr_ap else None
                
                with wc_l:
                    if dep_ap and dep_w:
                        st.markdown(f"""
                        <div class="glass-card">
                            <div style="display: flex; justify-content: space-between;">
                                <span style="font-size: 10px; font-weight: 700; color: #00d4ff;">ORIGIN: {dep_ap['iata']}</span>
                                <span style="font-size: 10px; color: var(--text-secondary);">{dep_ap['city']}</span>
                            </div>
                            <div style="display: flex; align-items: center; gap: 15px; margin-top: 10px;">
                                <div style="font-size: 24px;">{dep_w['emoji']}</div>
                                <div style="font-size: 28px; font-weight: 800;">{dep_w['temp_c']}°C</div>
                            </div>
                            <div style="font-size: 12px; color: var(--text-secondary); margin-top: 5px;">{dep_w['condition']} · Humidity {dep_w['humidity_pct']}%</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                with wc_r:
                    if arr_ap and arr_w:
                        st.markdown(f"""
                        <div class="glass-card">
                            <div style="display: flex; justify-content: space-between;">
                                <span style="font-size: 10px; font-weight: 700; color: #7b5ea7;">DESTINATION: {arr_ap['iata']}</span>
                                <span style="font-size: 10px; color: var(--text-secondary);">{arr_ap['city']}</span>
                            </div>
                            <div style="display: flex; align-items: center; gap: 15px; margin-top: 10px;">
                                <div style="font-size: 24px;">{arr_w['emoji']}</div>
                                <div style="font-size: 28px; font-weight: 800;">{arr_w['temp_c']}°C</div>
                            </div>
                            <div style="font-size: 12px; color: var(--text-secondary); margin-top: 5px;">{arr_w['condition']} · Humidity {arr_w['humidity_pct']}%</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Premium Features Row
                st.markdown("<br>", unsafe_allow_html=True)
                feat_tab1, feat_tab2, feat_tab3 = st.tabs(["🛡️ Intelligence", "🌱 Environmental", "🎒 Packing Guide"])
                
                with feat_tab1:
                    risk = assess_delay_risk(dep_w, arr_w)
                    st.markdown(f"""
                    <div style="display: flex; gap: 20px; align-items: flex-start;">
                        <div style="flex: 1;">
                            <h4 style="color: {risk['color']};">Risk Level: {risk['level']}</h4>
                            <p style="font-size: 14px; color: var(--text-secondary);">{risk['label']}</p>
                            <ul style="font-size: 13px; color: var(--text-secondary);">
                                {"".join([f"<li>{f}</li>" for f in risk['factors']]) if risk['factors'] else "<li>Minimal meteorological disruption detected.</li>"}
                            </ul>
                        </div>
                        <div style="flex: 1;">
                             <h4>Safety Indices</h4>
                             <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                                <div class="glass-card" style="padding: 15px;">
                                    <div style="font-size: 10px; color: var(--text-secondary);">UV INDEX</div>
                                    <div style="font-size: 20px; font-weight: 700;">{arr_w['uv_index'] if arr_w else 'N/A'}</div>
                                    <div style="font-size: 10px; color: #ffb300;">{uv_category(arr_w['uv_index'])[0] if arr_w else ''}</div>
                                </div>
                                <div class="glass-card" style="padding: 15px;">
                                    <div style="font-size: 10px; color: var(--text-secondary);">VISIBILITY</div>
                                    <div style="font-size: 20px; font-weight: 700;">{format_visibility(arr_w['visibility_m']) if arr_w else 'N/A'}</div>
                                </div>
                             </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with feat_tab2:
                    if flight['distance_km']:
                        carbon = estimate_carbon(flight['distance_km'])
                        st.markdown(f"""
                        <div class="glass-card" style="border-left: 4px solid #00e676;">
                            <h4 style="color: #00e676; margin: 0;">Carbon Footprint Analysis</h4>
                            <p style="font-size: 14px; color: var(--text-secondary); margin-top: 5px;">Estimated CO₂ emissions for this flight (Economy class).</p>
                            <div style="display: flex; justify-content: space-around; margin-top: 20px;">
                                <div style="text-align: center;">
                                    <div style="font-size: 28px; font-weight: 900;">{carbon['kg_co2']} kg</div>
                                    <div style="font-size: 11px; color: var(--text-secondary);">EMITTED CO₂</div>
                                </div>
                                <div style="text-align: center;">
                                    <div style="font-size: 28px; font-weight: 900;">{carbon['trees_equivalent']}</div>
                                    <div style="font-size: 11px; color: var(--text-secondary);">TREES TO ABSORB (1YR)</div>
                                </div>
                                <div style="text-align: center;">
                                    <div style="font-size: 28px; font-weight: 900;">{carbon['km_drive_equivalent']} km</div>
                                    <div style="font-size: 11px; color: var(--text-secondary);">DRIVING EQUIVALENT</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info("Route unknown. Please specify airports to see sustainability data.")
                
                with feat_tab3:
                    if arr_w and arr_ap:
                        packs = get_packing_suggestions(arr_w, arr_ap['city'])
                        st.markdown('<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px;">', unsafe_allow_html=True)
                        for p in packs:
                            st.markdown(f"""
                            <div class="glass-card" style="padding: 12px; display: flex; align-items: center; gap: 10px;">
                                <div style="font-size: 20px;">{p['icon']}</div>
                                <div>
                                    <div style="font-weight: 700; font-size: 13px;">{p['item']}</div>
                                    <div style="font-size: 10px; color: var(--text-secondary);">{p['reason']}</div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.info("Search result required for destination intelligence.")

        elif track_mode == "Route Search" and from_iata and to_iata:
             st.info("Route Search mode selected. Displaying comparative intelligence...")
             # (Logic for route search can be similarly expanded here)
             
        elif track_mode == "Airport Intelligence" and ap_query:
            results = search_airports(ap_query)
            if results:
                for ap in results:
                    st.markdown(f'<div class="glass-card" style="margin-bottom: 10px;">{ap["iata"]} - {ap["city"]}, {ap["country"]}</div>', unsafe_allow_html=True)
            else:
                st.error("No airports found.")
        else:
            st.warning("Please provide necessary inputs to begin tracking.")

    else:
        # Default State: Dashboard Preview
        st.markdown("""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div class="glass-card">
                <h4 style="margin: 0 0 10px 0;">Intelligence Suite</h4>
                <p style="font-size: 14px; color: var(--text-secondary);">Use the left command panel to track live flights or analyze global routes. Manver Aero Track provides millisecond-accurate tracking via OpenSky ADS-B network.</p>
            </div>
            <div class="glass-card">
                <h4 style="margin: 0 0 10px 0;">Destination Pulse</h4>
                <p style="font-size: 14px; color: var(--text-secondary);">Compare temperatures, humidity, and UV safety across airports. Get smart packing recommendations based on real-time meteorological forecasts.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ─── Global Footer ───────────────────────────────────────────────────────────
st.markdown("""
<br><br>
<div style="text-align: center; color: var(--text-secondary); font-size: 12px; border-top: 1px solid var(--border); padding-top: 20px;">
    MANVER AERO TRACK · Open Source Intelligence Suite · v1.2 Premium<br>
    Built with Folium, OpenSky Network, and Open-Meteo REST APIs.
</div>
""", unsafe_allow_html=True)
