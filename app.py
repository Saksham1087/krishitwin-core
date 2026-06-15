import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk

# --- 👑 CONFIG & THEME OVERHAUL ---
st.set_page_config(
    page_title="KrishiTwin OS — NextGen National Command Deck", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Advanced UI Glassmorphism & Cyber-Glow Aesthetics
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&display=swap');
    
    .main { background-color: #0B0F19; color: #E2E8F0; font-family: 'Inter', sans-serif; }
    
    /* Premium Glassmorphic Cards */
    .premium-card { 
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        padding: 24px; 
        border-radius: 16px; 
        border: 1px solid #334155; 
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }
    
    .metric-title { font-size: 13px; text-transform: uppercase; letter-spacing: 0.1em; color: #94A3B8; font-weight: 600; }
    .metric-value-huge { font-size: 32px; font-weight: 700; font-family: 'JetBrains Mono', monospace; margin-top: 5px; }
    
    /* Neon Status Badges */
    .badge-critical { background: rgba(239, 68, 68, 0.15); color: #F87171; border: 1px solid rgba(239, 68, 68, 0.4); padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; display: inline-block; }
    .badge-warning { background: rgba(245, 158, 11, 0.15); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.4); padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; display: inline-block; }
    .badge-stable { background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.4); padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; display: inline-block; }
    
    /* Cyber Sidebar Fixes */
    .stSidebar { background-color: #0F172A !important; border-right: 1px solid #1E293B; }
    h1, h2, h3 { font-weight: 700; color: #FFFFFF; letter-spacing: -0.02em; }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0B0F19; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
    </style>
""", unsafe_allow_html=True)

# --- 🗺️ EXPANDED RELATIONAL GEO-GRAPH ---
state_city_map = {
    "Maharashtra": {
        "cities": {
            "Nashik Grape/Onion Belt": {"lat": 19.9975, "lon": 73.7898},
            "Chhatrapati Sambhaji Nagar Sector": {"lat": 19.8762, "lon": 75.3433},
            "Pune Sugarcane Basin": {"lat": 18.5204, "lon": 73.8567}
        }
    },
    "Punjab": {
        "cities": {
            "Ludhiana Central Hub": {"lat": 30.9010, "lon": 75.8573},
            "Bathinda Wheat Zone": {"lat": 30.2110, "lon": 74.9454},
            "Amritsar Agro Perimeter": {"lat": 31.6340, "lon": 74.8723}
        }
    },
    "Gujarat": {
        "cities": {
            "Surat Cotton Basin": {"lat": 21.1702, "lon": 72.8311},
            "Anand Dairy/Agri Command": {"lat": 22.5645, "lon": 72.9289},
            "Rajkot Groundnut Sector": {"lat": 22.3039, "lon": 70.8022}
        }
    },
    "Uttar Pradesh": {
        "cities": {
            "Gorakhpur Sugar Basin": {"lat": 26.7606, "lon": 83.3731},
            "Bareilly Paddy Plains": {"lat": 28.3670, "lon": 79.4304},
            "Varanasi Vegetable Cluster": {"lat": 25.3176, "lon": 82.9739}
        }
    },
    "Andhra Pradesh": {
        "cities": {
            "Guntur Chilli/Paddy Delta": {"lat": 16.3067, "lon": 80.4365},
            "Kurnool Rayalaseema Sector": {"lat": 15.8281, "lon": 78.0373},
            "Nellore Aqua/Rice Hub": {"lat": 14.4426, "lon": 79.9865}
        }
    }
}

# --- 🎮 SIDEBAR Control Deck ---
st.sidebar.markdown("## 🛰️ GEO-COMMAND ENGINE")
selected_state = st.sidebar.selectbox("🗺️ Select State Matrix:", list(state_city_map.keys()))
available_cities = list(state_city_map[selected_state]["cities"].keys())
selected_city = st.sidebar.selectbox("📍 Select Municipal Hub:", available_cities)

st.sidebar.markdown("---")
st.sidebar.markdown("## 🎛️ SIMULATION MATRIX")
climate_anomaly = st.sidebar.toggle("🚨 Force Climate Anomaly Mode", value=False)

# Updated options to align with token-free carto tile layers
map_style = st.sidebar.selectbox("🎨 Map Topology Canvas:", ["Dark Cyber Canvas", "Light Tech Canvas"])

crop_filter = st.sidebar.multiselect(
    "🌾 Targeted Crop Profiles:", 
    options=['Kharif Rice', 'Cotton', 'Sugarcane', 'Pulses'], 
    default=['Kharif Rice', 'Cotton', 'Sugarcane', 'Pulses']
)

# FIXED: Resolves background to open-source CartoDB styles that don't look for a Mapbox configuration token
pdk_style = "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"
if map_style == "Light Tech Canvas":
    pdk_style = "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"

# --- 🛰️ SIMULATION ENGINE DATA GENERATION ---
def generate_focused_city_data(state_name, city_name, anomaly_mode):
    city_coords = state_city_map[state_name]["cities"][city_name]
    crops = ['Kharif Rice', 'Cotton', 'Sugarcane', 'Pulses']
    data = []
    np.random.seed(len(city_name))
    
    for i in range(1, 7):
        block_label = f"Vector Plot Sector-{i:02d}"
        crop = np.random.choice(crops)
        
        ndvi = round(np.random.uniform(0.38, 0.88), 2)
        ndwi = round(np.random.uniform(0.15, 0.60), 2)
        demand_etc = round(np.random.uniform(32.0, 55.0), 1)
        
        if anomaly_mode:
            ndwi = round(max(0.01, ndwi - 0.28), 2)
            demand_etc = round(demand_etc * 1.42, 1)
            
        actual_et = round(demand_etc * (ndwi + 0.40), 1)
        if actual_et > demand_etc: actual_et = demand_etc
        water_deficit = round(demand_etc - actual_et, 1)
        
        risk_index = int(min(100, max(0, (water_deficit / demand_etc) * 100 + (30 if anomaly_mode else 0))))
        
        if ndvi < 0.45: stage = "Vegetative Emergence"
        elif ndvi < 0.75: stage = "Mid-Season Reproductive"
        else: stage = "Late Maturation Window"
        
        lat_scatter = city_coords['lat'] + np.random.uniform(-0.018, 0.018)
        lon_scatter = city_coords['lon'] + np.random.uniform(-0.018, 0.018)
        
        if water_deficit > 15.0:
            color_rgb = [239, 68, 68, 220]
            severity = "Critical Alert"
        elif water_deficit > 6.0:
            color_rgb = [245, 158, 11, 220]
            severity = "Elevated Warning"
        else:
            color_rgb = [16, 185, 129, 220]
            severity = "Operational Stability"
            
        data.append({
            "Command Sector Node": block_label,
            "Crop Class": crop,
            "NDVI (Vigour)": ndvi,
            "NDWI (Moisture)": ndwi,
            "8-Day Demand (mm)": demand_etc,
            "Actual ET (mm)": actual_et,
            "Water Deficit (mm)": water_deficit,
            "Climate Risk Index (%)": risk_index,
            "Phenology Stage": stage,
            "Severity": severity,
            "latitude": lat_scatter,
            "longitude": lon_scatter,
            "fill_color": color_rgb
        })
    return pd.DataFrame(data)

df_raw = generate_focused_city_data(selected_state, selected_city, climate_anomaly)
df_matrix = df_raw[df_raw["Crop Class"].isin(crop_filter)]

# --- 🖥️ CORE INTERFACE VIEW LAYOUT ---
st.title("🛡️ KrishiTwin OS — Precision Command Console")
st.markdown(f"📡 Regional Node Infrastructure Pipeline: <span style='color:#10B981; font-weight:bold;'>{selected_state}</span> Domain ➔ <span style='color:#3B82F6; font-weight:bold;'>{selected_city} Command Hub</span>", unsafe_allow_html=True)
st.write("---")

# Premium Metrics Panel
alert_count = len(df_matrix[df_matrix["Severity"] == "Critical Alert"])
avg_risk = int(df_matrix["Climate Risk Index (%)"].mean()) if not df_matrix.empty else 0
max_deficit = df_matrix["Water Deficit (mm)"].max() if not df_matrix.empty else 0

m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    st.markdown(f"""<div class="premium-card">
        <div class="metric-title">📡 Active Target Node</div>
        <div class="metric-value-huge" style="color:#3B82F6; font-size:20px;">{selected_city}</div>
    </div>""", unsafe_allow_html=True)
with m_col2:
    st.markdown(f"""<div class="premium-card">
        <div class="metric-title">🔥 Mean Regional Risk Index</div>
        <div class="metric-value-huge" style="color:{'#EF4444' if avg_risk > 60 else '#F59E0B' if avg_risk > 35 else '#10B981'};">{avg_risk}%</div>
    </div>""", unsafe_allow_html=True)
with m_col3:
    st.markdown(f"""<div class="premium-card">
        <div class="metric-title">⚠️ Hot Spot Threat Alert Count</div>
        <div class="metric-value-huge" style="color:{'#EF4444' if alert_count > 0 else '#10B981'};">{alert_count} Threats</div>
    </div>""", unsafe_allow_html=True)
with m_col4:
    st.markdown(f"""<div class="premium-card">
        <div class="metric-title">💧 Peak Sector Deficit</div>
        <div class="metric-value-huge" style="color:#22D3EE;">{max_deficit} mm</div>
    </div>""", unsafe_allow_html=True)

# Split Layout
left_workspace, right_workspace = st.columns([2, 1])

with left_workspace:
    st.markdown("### 🗺️ Hyper-Local Geospatial Vector Array Map")
    if not df_matrix.empty:
        target_center = state_city_map[selected_state]["cities"][selected_city]
        
        view_state = pdk.ViewState(
            latitude=target_center['lat'], 
            longitude=target_center['lon'], 
            zoom=12.2, 
            pitch=45,
            bearing=-10
        )
        
        map_df = df_matrix.copy()
        map_df['elevation_metric'] = map_df["Water Deficit (mm)"]
        map_df['color_vector'] = map_df["fill_color"]
        
        layer = pdk.Layer(
            "ColumnLayer",
            data=map_df,
            get_position="[longitude, latitude]",
            get_elevation="elevation_metric",
            elevation_scale=70,
            radius=150,
            get_fill_color="color_vector",
            pickable=True,
            auto_highlight=True
        )
        
        st.pydeck_chart(pdk.Deck(
            map_style=pdk_style,
            layers=[layer], 
            initial_view_state=view_state,
            tooltip={"text": "Sector Unit: {Command Sector Node}\nCrop Profile: {Crop Class}\nRisk Index: {Climate Risk Index (%)}%\nDeficit Parameter: {Water Deficit (mm)}mm"}
        ))
    else:
        st.warning("No localized vector lines match current filter criteria.")

    st.markdown("### 📋 Real-Time Regional Sector Ledger")
    st.dataframe(
        df_matrix.drop(columns=['latitude', 'longitude', 'fill_color']), 
        use_container_width=True, 
        height=220
    )

with right_workspace:
    st.markdown("### ⚡ AI System Directives & Logistics")
    
    available_sectors = df_matrix["Command Sector Node"].unique() if not df_matrix.empty else ["None"]
    selected_sector = st.selectbox("🎯 Target Live Monitoring Vector:", available_sectors)
    
    if selected_sector != "None":
        block_row = df_matrix[df_matrix["Command Sector Node"] == selected_sector].iloc[0]
        deficit = block_row["Water Deficit (mm)"]
        risk_val = block_row["Climate Risk Index (%)"]
        
        if "Critical" in block_row["Severity"]:
            badge_html = f'<span class="badge-critical">🛑 EMERGENCY LEVEL Threat</span>'
            directive_text = f"🚨 **CRITICAL INTERVENTION MANDATE:** Sector **{selected_sector}** shows a massive **{risk_val}%** risk probability. Open primary distributary sluice lines immediately to mitigate biomass failure risk."
        elif "Warning" in block_row["Severity"]:
            badge_html = f'<span class="badge-warning">⚠️ ELEVATED STRESS RISK</span>'
            directive_text = f"⚡ **PREVENTATIVE LOGISTICS DEPLOYMENT:** Moisture levels falling inside **{selected_sector}**. Schedule automated gate system rotation loops over the coming 24-hour cycle."
        else:
            badge_html = f'<span class="badge-stable">✅ ZONE STABLE</span>'
            directive_text = f"🌱 **EQUILIBRIUM MAINTAINED:** Crop metrics for **{selected_sector}** remain safely inside target operational ranges. Continuous observation sequence active."

        st.markdown(f"""<div class="premium-card">
            <h4>Plot ID: {selected_sector}</h4>
            <hr style="border-color:#334155; margin:10px 0;">
            <p>🌾 Crop Category: <b>{block_row["Crop Class"]}</b></p>
            <p>📈 Satellite Growth Phase: <i>{block_row["Phenology Stage"]}</i></p>
            <p>🔥 Climate Anomaly Threat Index: <b>{risk_val}%</b></p>
            <div style="margin-top:10px;">{badge_html}</div>
        </div>""", unsafe_allow_html=True)
        
        st.markdown("#### Automated System Order Log:")
        st.info(directive_text)
        
        st.markdown("---")
        st.markdown("#### 📄 Document Generation Center")
        
        comprehensive_report = f"""========================================================================
🛡️ KRISHITWIN OS CENTRAL COMMAND LOGISTICS ADVISORY BRIEF
========================================================================
Generated Operational Timestamp: Live Telemetry Stream
Target Region Domain            : {selected_state} State Jurisdiction
Target Local Command Hub       : {selected_city}
Selected Monitoring Plot       : {selected_sector}
------------------------------------------------------------------------
SATELLITE TELEMETRY ANALYSIS MATRIX:
------------------------------------------------------------------------
* Target Crop Classification  : {block_row["Crop Class"]}
* Phenological Crop Stage      : {block_row["Phenology Stage"]}
* Normalized Veg Index (NDVI)  : {block_row['NDVI (Vigour)']}
* Water Deficit Parameter      : {deficit} mm
* Consolidated Risk Matrix     : {risk_val}% Risk Factor
* Operational Evaluation Class : {block_row["Severity"]}

------------------------------------------------------------------------
SYSTEM DIRECTIVE BRIEF ORDER:
------------------------------------------------------------------------
{directive_text}

------------------------------------------------------------------------
END OF SYSTEM ADVISORY BRIEF LOG
========================================================================
"""
        st.download_button(
            label="📥 Export Municipal Advisory Command Brief",
            data=comprehensive_report,
            file_name=f"KrishiTwin_Advisory_{selected_sector.replace(' ', '_')}.txt",
            mime="text/plain"
        )
