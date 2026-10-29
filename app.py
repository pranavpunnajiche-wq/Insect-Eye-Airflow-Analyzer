import math
from datetime import datetime

import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import pandas as pd


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Insect Eye - Airflow Analyzer",
    page_icon="🦟",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS - DARK NAVY DASHBOARD
# =========================================================

st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #001326;
        color: #e5f2ff;
    }

    [data-testid="stHeader"] {
        background-color: #061d35;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #092744, #00182e);
        border-right: 1px solid #174568;
    }

    [data-testid="stSidebar"] * {
        color: #e5f2ff;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1800px;
    }

    .hero {
        background: linear-gradient(110deg, #0c2b4b, #061b32);
        border: 1px solid #153d60;
        border-radius: 10px;
        padding: 15px 22px;
        margin-bottom: 14px;
    }

    .hero-title {
        color: #d8edff;
        font-size: 27px;
        font-weight: 750;
        margin: 0;
    }

    .hero-subtitle {
        color: #b9d8f3;
        font-size: 13px;
        margin-top: 5px;
    }

    .status {
        color: #00e68a;
        font-weight: bold;
        text-align: right;
    }

    .status-small {
        color: #c3d9ed;
        text-align: right;
        font-size: 11px;
    }

    .section-card {
        background: #041c32;
        border: 1px solid #174567;
        border-radius: 9px;
        padding: 12px;
        margin-bottom: 10px;
    }

    .section-title {
        font-size: 17px;
        font-weight: 700;
        color: #e1f0ff;
        margin-bottom: 12px;
    }

    .metric-card {
        background: linear-gradient(145deg, #0b2b49, #08233d);
        border: 1px solid #194766;
        border-radius: 9px;
        padding: 13px 12px;
        min-height: 92px;
        margin-bottom: 8px;
    }

    .metric-label {
        font-size: 12px;
        color: #c4def4;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 23px;
        font-weight: 750;
        color: #f2f8ff;
        line-height: 1.2;
    }

    .metric-note {
        color: #b7d2eb;
        font-size: 11px;
        margin-top: 4px;
    }

    .good {
        color: #00efa0;
        font-size: 15px;
        font-weight: bold;
    }

    .log-box {
        background: #031a2e;
        border: 1px solid #174567;
        border-radius: 8px;
        padding: 12px;
        color: #bdd8ef;
        font-family: monospace;
        font-size: 11px;
        line-height: 1.7;
    }

    .footer {
        color: #a9c8e2;
        font-size: 11px;
        padding: 12px 5px;
        border-top: 1px solid #143957;
        margin-top: 8px;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #041c32;
        border-color: #174567;
        border-radius: 9px;
    }

    div[data-testid="stMetric"] {
        background: #08233d;
        border: 1px solid #194766;
        border-radius: 8px;
        padding: 10px;
    }

    div[data-testid="stMetricLabel"] {
        color: #c4def4;
    }

    div[data-testid="stMetricValue"] {
        color: #f2f8ff;
    }

    .stButton button {
        background: #0879ff;
        color: white;
        border: 1px solid #1687ff;
        border-radius: 7px;
        font-weight: 650;
        width: 100%;
    }

    .stButton button:hover {
        background: #0065df;
        color: white;
        border-color: #51a4ff;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #194766;
        border-radius: 7px;
    }

    h1, h2, h3 {
        color: #e5f2ff;
    }

    .small-note {
        color: #a8c8e2;
        font-size: 11px;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR CONTROLS
# =========================================================

with st.sidebar:

    st.markdown("## 🦟 Insect Eye")

    st.markdown("---")
    st.markdown("### 1. Pressure Readings (Pa)")

    total_pressure = st.number_input(
        "Total Pressure (Pt)",
        min_value=0.0,
        value=101520.0,
        step=1.0
    )

    static_pressure = st.number_input(
        "Static Pressure (Ps)",
        min_value=0.0,
        value=101485.0,
        step=1.0
    )

    st.markdown("---")
    st.markdown("### 2. Air Properties")

    air_density = st.number_input(
        "Air Density (kg/m³)",
        min_value=0.1,
        max_value=2.0,
        value=1.225,
        step=0.001,
        format="%.3f"
    )

    temperature = st.number_input(
        "Temperature (°C)",
        min_value=-50.0,
        max_value=100.0,
        value=20.0,
        step=1.0
    )

    st.markdown("---")
    st.markdown("### 3. Aerofoil Settings")

    angle = st.slider(
        "Angle of Attack (°)",
        min_value=-10,
        max_value=20,
        value=5
    )

    reference_speed = st.slider(
        "Air Speed (m/s) [Reference]",
        min_value=1.0,
        max_value=20.0,
        value=5.0,
        step=0.5
    )

    st.markdown("---")
    st.markdown("### 4. Sensor Grid (Insect Eye)")

    grid_size = st.selectbox(
        "Grid Size",
        options=[10, 20, 30, 40],
        index=1,
        format_func=lambda n: f"{n} × {n} ({n*n} sensors)"
    )

    vortex_strength = st.slider(
        "Vortex Strength",
        min_value=1.0,
        max_value=10.0,
        value=5.0,
        step=0.5
    )

    run_analysis = st.button(
        "▶  Run Analysis",
        use_container_width=True
    )


# =========================================================
# CALCULATIONS
# =========================================================

dynamic_pressure = total_pressure - static_pressure

valid_pressure = dynamic_pressure >= 0

if valid_pressure:
    airspeed = math.sqrt(
        2.0 * dynamic_pressure / air_density
    )
    airspeed_kmh = airspeed * 3.6
else:
    airspeed = 0.0
    airspeed_kmh = 0.0


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="hero">
    <div class="hero-title">🦟 Insect Eye - Airflow Analyzer</div>
    <div class="hero-subtitle">
        Pitot-equivalent Calculations
        &nbsp; | &nbsp; Optical Flow Array
        &nbsp; | &nbsp; Micro-Vortex Detection
    </div>
</div>
""", unsafe_allow_html=True)

status_col, _ = st.columns([1, 5])

with status_col:
    st.markdown(
        '<div class="status">🟢 System Ready</div>'
        '<div class="status-small">Software Simulation</div>',
        unsafe_allow_html=True
    )


# =========================================================
# CALCULATED AIRFLOW PARAMETERS
# =========================================================

st.markdown(
    '<div class="section-title">'
    '🌀 Calculated Airflow Parameters'
    '</div>',
    unsafe_allow_html=True
)

if not valid_pressure:
    st.error(
        "Total pressure is below static pressure. "
        "Please correct your input values."
    )

# First row: four metrics
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">🌬 Estimated Airspeed</div>
            <div class="metric-value">{airspeed:.2f} m/s</div>
            <div class="metric-note">{airspeed_kmh:.2f} km/h</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">◉ Dynamic Pressure</div>
            <div class="metric-value">{dynamic_pressure:.2f} Pa</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">◉ Total Pressure (Pt)</div>
            <div class="metric-value">{total_pressure:.0f} Pa</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">◉ Static Pressure (Ps)</div>
            <div class="metric-value">{static_pressure:.0f} Pa</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# Second row: air properties and quality
p1, p2, p3 = st.columns([1, 1, 1.4])

with p1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">🛡 Air Density (ρ)</div>
            <div class="metric-value">{air_density:.3f} kg/m³</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with p2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">🌡 Temperature (T)</div>
            <div class="metric-value">{temperature:.1f} °C</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with p3:
    quality = "Good" if valid_pressure else "Check Inputs"
    quality_color = "#00efa0" if valid_pressure else "#ff7777"

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">🍃 Flow Quality</div>
            <div class="metric-value" style="color:{quality_color}">
                {quality}
            </div>
            <div class="metric-note">
                {"Inputs mathematically valid" if valid_pressure
                 else "Invalid pressure difference"}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# SIMULATED FLOW FIELD
# =========================================================

x = np.linspace(-1.0, 3.5, grid_size)
y = np.linspace(-1.5, 1.5, grid_size)

X, Y = np.meshgrid(x, y)

# Rotating flow around two possible vortex centres
vortex_x = 0.5
vortex_y = 0.0

dx = X - vortex_x
dy = Y - vortex_y

distance = dx**2 + dy**2 + 0.12

U = reference_speed - vortex_strength * dy / distance
V = vortex_strength * dx / distance

# Calculate vorticity of the simulated field
dV_dy, dV_dx = np.gradient(V, y, x)
dU_dy, dU_dx = np.gradient(U, y, x)

vorticity = dV_dx - dU_dy

speed_field = np.sqrt(U**2 + V**2)


# =========================================================
# MIDDLE ROW: AEROFOIL AND OPTICAL FLOW
# =========================================================

left_panel, right_panel = st.columns([1.55, 1])

with left_panel:

    st.markdown(
        '<div class="section-title">'
        '🌬 Airflow Visualization (Aerofoil)'
        '</div>',
        unsafe_allow_html=True
    )

    fig1, ax1 = plt.subplots(figsize=(8, 4.3))

    fig1.patch.set_facecolor("#041c32")
    ax1.set_facecolor("#041c32")

    # Build an illustrative velocity field around an aerofoil
    xa = np.linspace(-1.0, 3.5, 150)
    ya = np.linspace(-1.5, 1.5, 100)

    XA, YA = np.meshgrid(xa, ya)

    ua = np.ones_like(XA) * reference_speed

    angle_rad = np.radians(angle)

    upper = np.exp(
        -((YA - 0.35) ** 2) / 0.15
        - ((XA - 0.7) ** 2) / 0.7
    )

    lower = np.exp(
        -((YA + 0.35) ** 2) / 0.15
        - ((XA - 0.7) ** 2) / 0.7
    )

    va = (
        (upper - lower) * reference_speed * 0.8
        + np.sin(angle_rad) * reference_speed * 0.3
    )

    velocity = np.sqrt(ua**2 + va**2)

    contour = ax1.contourf(
        XA,
        YA,
        velocity,
        levels=35,
        cmap="jet"
    )

    ax1.streamplot(
        xa,
        ya,
        ua,
        va,
        color="white",
        density=1.1,
        linewidth=0.6,
        arrowsize=0.8
    )

    # Aerofoil outline
    foil_x = np.linspace(0, 2, 200)
    foil_y = (
        0.15
        * np.sin(np.pi * foil_x / 2)
        * (1 - 0.2 * foil_x)
    )

    ax1.fill_between(
        foil_x,
        foil_y - 0.035,
        foil_y + 0.035,
        color="#dbe9f6",
        edgecolor="white"
    )

    ax1.set_xlabel("X Position (m)", color="#dcecff")
    ax1.set_ylabel("Y Position (m)", color="#dcecff")
    ax1.tick_params(colors="#c9dff4")
    ax1.set_xlim(-1, 3.5)
    ax1.set_ylim(-1.5, 1.5)

    for spine in ax1.spines.values():
        spine.set_color("#2b5878")

    cb1 = fig1.colorbar(contour, ax=ax1, pad=0.03)
    cb1.set_label("Illustrative Velocity (m/s)", color="#dcecff")
    cb1.ax.tick_params(colors="#dcecff")

    fig1.tight_layout()
    st.pyplot(fig1, use_container_width=True)
    plt.close(fig1)


with right_panel:

    st.markdown(
        '<div class="section-title">'
        '🔷 Optical Flow Array (Insect Eye)'
        '</div>',
        unsafe_allow_html=True
    )

    fig2, ax2 = plt.subplots(figsize=(5.4, 4.3))

    fig2.patch.set_facecolor("#041c32")
    ax2.set_facecolor("#00152b")

    strength = np.sqrt(U**2 + V**2)

    ax2.quiver(
        X,
        Y,
        U,
        V,
        strength,
        cmap="jet",
        angles="xy",
        scale_units="xy",
        scale=max(reference_speed * 2, 1),
        width=0.004
    )

    ax2.set_title(
        f"{grid_size} × {grid_size} Simulated Array",
        color="#e5f2ff",
        fontsize=10
    )

    ax2.set_xlabel("X Position", color="#dcecff")
    ax2.set_ylabel("Y Position", color="#dcecff")
    ax2.tick_params(colors="#c9dff4")

    for spine in ax2.spines.values():
        spine.set_color("#2b5878")

    ax2.set_aspect("equal", adjustable="box")

    fig2.tight_layout()
    st.pyplot(fig2, use_container_width=True)
    plt.close(fig2)


# =========================================================
# BOTTOM ROW: SENSOR TABLE AND VORTEX HEATMAP
# =========================================================

table_panel, vortex_panel = st.columns([1, 1.25])

with table_panel:

    st.markdown(
        '<div class="section-title">'
        '📋 Sensor Readings (Sample)'
        '</div>',
        unsafe_allow_html=True
    )

    # Flatten the simulated sensor grid into rows
    records = []

    for row in range(grid_size):
        for col in range(grid_size):

            vx = float(U[row, col])
            vy = float(V[row, col])

            records.append({
                "Sensor ID": f"S{row * grid_size + col + 1:03d}",
                "X (m)": round(float(X[row, col]), 2),
                "Y (m)": round(float(Y[row, col]), 2),
                "Vx (m/s)": round(vx, 2),
                "Vy (m/s)": round(vy, 2),
                "Speed (m/s)": round(
                    math.sqrt(vx**2 + vy**2), 2
                )
            })

    sensor_df = pd.DataFrame(records)

    st.dataframe(
        sensor_df.head(5),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        f"Showing 5 of {grid_size * grid_size} simulated sensors."
    )


with vortex_panel:

    st.markdown(
        '<div class="section-title">'
        '🦟 Micro-Vortex Detection'
        '</div>',
        unsafe_allow_html=True
    )

    fig3, ax3 = plt.subplots(figsize=(7, 4.1))

    fig3.patch.set_facecolor("#041c32")
    ax3.set_facecolor("#00152b")

    heat = ax3.contourf(
        X,
        Y,
        vorticity,
        levels=35,
        cmap="jet"
    )

    # Mark the centre of the simulated rotating field
    ax3.scatter(
        [vortex_x],
        [vortex_y],
        s=100,
        facecolors="none",
        edgecolors="red",
        linewidths=2,
        label="Simulated vortex centre"
    )

    # Aerofoil outline for visual reference
    ax3.fill_between(
        foil_x,
        foil_y - 0.035,
        foil_y + 0.035,
        color="#dbe9f6",
        edgecolor="white"
    )

    ax3.set_xlabel("X Position (m)", color="#dcecff")
    ax3.set_ylabel("Y Position (m)", color="#dcecff")
    ax3.tick_params(colors="#c9dff4")

    for spine in ax3.spines.values():
        spine.set_color("#2b5878")

    cb3 = fig3.colorbar(heat, ax=ax3, pad=0.03)
    cb3.set_label("Vorticity (1/s)", color="#dcecff")
    cb3.ax.tick_params(colors="#dcecff")

    ax3.legend(
        loc="upper right",
        fontsize=7,
        facecolor="#092744",
        labelcolor="white"
    )

    fig3.tight_layout()
    st.pyplot(fig3, use_container_width=True)
    plt.close(fig3)


# =========================================================
# SYSTEM LOG
# =========================================================

st.markdown(
    '<div class="section-title">🟢 System Log</div>',
    unsafe_allow_html=True
)

now = datetime.now().strftime("%H:%M:%S")

log_text = f"""
[{now}] Pressure inputs received
[{now}] Airspeed calculation: {airspeed:.2f} m/s
[{now}] Optical flow grid processed ({grid_size * grid_size} simulated points)
[{now}] Vorticity analysis completed
[{now}] Dashboard analysis complete
"""

st.markdown(
    f'<div class="log-box">{log_text.replace(chr(10), "<br>")}</div>',
    unsafe_allow_html=True
)


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    🦟 Insect Eye Inspired
    &nbsp;&nbsp; | &nbsp;&nbsp; Smart Sensing
    &nbsp;&nbsp; | &nbsp;&nbsp; Better Airflow Insights
    <br><br>
    Software Prototype &nbsp; | &nbsp;
    Not Connected to Physical Hardware
</div>
""", unsafe_allow_html=True)
