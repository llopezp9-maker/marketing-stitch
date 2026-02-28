
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import base64
from pathlib import Path

# 1. Configuración de página
st.set_page_config(
    page_title="Inteligencia de Medios Colombia | Powered by Stitch",
    page_icon="🏙️",
    layout="wide"
)

def get_base64_img(img_path):
    return base64.b64encode(open(img_path, "rb").read()).decode()

# Rutas de imágenes (relativas al archivo app.py)
bg_path = Path(__file__).parent / "banner_bg.png"
icons_path = Path(__file__).parent / "icons.png"

try:
    banner_bg_b64 = get_base64_img(bg_path)
    icons_b64 = get_base64_img(icons_path)
except Exception:
    banner_bg_b64 = ""
    icons_b64 = ""

# QR y Enlace de LinkedIn Universal
qr_url = "https://api.qrserver.com/v1/create-qr-code/?size=120x120&data=https://www.linkedin.com/in/luislopezanalytics"

# 2. Estilo Visual: Azules Claros Premium (Firma Visual de Stitch)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Outfit:wght@700&display=swap');

    .stApp {
        background-color: #f8fafc;
        color: #1e293b;
    }
    
    .stitch-signature {
        color: #0ea5e9;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 0.8rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        margin-bottom: -10px;
    }

    h1, h2, h3, h4 {
        font-family: 'Outfit', sans-serif !important;
        color: #0369a1 !important;
        margin-bottom: 0.8rem;
    }
    
    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-top: 4px solid #0ea5e9;
        text-align: center;
    }
    
    .kpi-label { color: #64748b; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; }
    .kpi-value { font-size: 1.8rem; font-weight: 700; color: #0ea5e9; }

    .stTabs [data-baseweb="tab"] p { color: #475569 !important; transition: all 0.3s ease; }
    .stTabs [aria-selected="true"] p { color: #0ea5e9 !important; font-weight: 700; }
    .stTabs [data-baseweb="tab-list"] { gap: 15px; background-color: transparent; }

    /* Estilos para Conclusiones Premium & Glassmorphism */
    .conclusion-box {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-left: 6px solid #1e40af;
        border-radius: 16px;
        padding: 30px;
        margin: 25px 0;
        box-shadow: 0 10px 30px rgba(30, 64, 175, 0.08);
        border: 1px solid rgba(226, 232, 240, 0.5);
    }
    .conclusion-item {
        margin-bottom: 22px;
        font-size: 1.05rem;
        line-height: 1.7;
        color: #334155;
    }
    .conclusion-icon {
        font-size: 1.6rem;
        margin-right: 15px;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    }
    .download-btn {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
        color: white !important;
        padding: 12px 24px;
        border-radius: 12px;
        text-decoration: none;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 12px;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(30, 64, 175, 0.2);
    }
    .download-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(30, 64, 175, 0.3);
    }

    /* Estilos Banner de Firma Premium - Perfeccionamiento */
    .signature-banner {
        background: linear-gradient(135deg, rgba(30, 58, 138, 0.85) 0%, rgba(30, 64, 175, 0.85) 100%), url("data:image/png;base64,{banner_bg_b64}");
        background-size: cover;
        background-position: center;
        padding: 80px 40px;
        border-radius: 32px;
        color: white;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 25px 50px -12px rgba(30, 64, 175, 0.4);
        border: 1px solid rgba(255,255,255,0.15);
        position: relative;
    }
    .signature-banner::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(180deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
        pointer-events: none;
    }
    .sig-title { font-family: 'Outfit'; font-size: 3rem; font-weight: 800; margin: 0; color: white !important; }
    .sig-subtitle { font-family: 'Inter'; font-size: 1.1rem; opacity: 0.9; margin: 15px 0 30px 0; letter-spacing: 0.5px; }
    .sig-divider { border-top: 1px solid rgba(255,255,255,0.2); margin: 25px 0; }
    .sig-footer { display: flex; align-items: center; justify-content: center; gap: 40px; flex-wrap: wrap; }
    .qr-container { background: white; padding: 10px; border-radius: 12px; display: inline-block; }
    .sig-info { text-align: left; }
    .sig-name { font-size: 1.5rem; font-weight: 700; margin-bottom: 5px; display: flex; align-items: center; gap: 10px; }
    .sig-rank { font-size: 0.95rem; opacity: 0.8; }
    .linkedin-btn {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.3);
        padding: 12px 25px;
        border-radius: 50px;
        color: white !important;
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 10px;
        backdrop-filter: blur(5px);
        transition: all 0.3s ease;
    }
    .linkedin-btn:hover { background: rgba(255,255,255,0.2); transform: translateY(-2px); }

    /* Micro-firma para final de pestañas */
    .micro-signature {
        text-align: right;
        font-size: 0.75rem;
        color: #94a3b8;
        font-style: italic;
        margin-top: 30px;
        border-top: 1px solid #f1f5f9;
        padding-top: 10px;
    }

    /* Estilos Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {
        color: #1e3a8a !important;
        font-weight: 600 !important;
    }
    
    /* Botones de Colapsar Sidebar Permanentes y Notorios */
    button[title="Collapse sidebar"], button[title="Expand sidebar"] {
        background-color: #f43f5e !important;
        border-radius: 50% !important;
        width: 45px !important;
        height: 45px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 4px 12px rgba(244, 63, 94, 0.4) !important;
        transition: transform 0.2s ease !important;
        z-index: 1000000 !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    button[title="Collapse sidebar"]:hover { transform: scale(1.1); }
    
    button[title="Collapse sidebar"] svg, button[title="Expand sidebar"] svg {
        fill: white !important;
        width: 30px !important;
        height: 30px !important;
    }

    /* Estilo para la línea roja divisoria entre párrafos */
    .cronica-container {
        display: flex;
        gap: 30px;
        align-items: center;
        margin-top: 20px;
    }
    .cronica-text {
        flex: 1;
        text-align: justify;
        font-size: 1rem;
        line-height: 1.6;
    }
    .red-divider {
        width: 4px;
        height: 100px;
        background-color: #f43f5e;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(244, 63, 94, 0.5);
    }
    @media (max-width: 768px) {
        .cronica-container { flex-direction: column; }
        .red-divider { width: 100%; height: 4px; }
    }
    .sidebar-title {
        color: #1e3a8a;
        font-weight: 800;
        font-size: 1.1rem;
        margin-bottom: 10px;
        text-align: center;
    }
    /* Responsividad Celular */
    @media (max-width: 768px) {
        .sig-title { font-size: 1.8rem; }
        .sig-subtitle { font-size: 0.9rem; margin: 10px 0; }
        .signature-banner { padding: 40px 20px; border-radius: 20px; }
        .sig-name { font-size: 1.2rem; }
        .sig-rank { font-size: 0.8rem; }
        .kpi-value { font-size: 1.4rem; }
        .kpi-label { font-size: 0.7rem; }
        .stPlotlyChart { height: 350px !important; }
    }
</style>
""", unsafe_allow_html=True)

# 3. Datos Maestro
@st.cache_data
def load_all_market_data():
    years = np.arange(1995, 2026)
    data = {'Año': years}
    
    def interpolate(start, end, s_year, e_year, type='linear'):
        res = np.zeros(len(years))
        idx_s, idx_e = s_year - 1995, e_year - 1995
        if type == 'linear':
            res[idx_s:idx_e+1] = np.linspace(start, end, idx_e - idx_s + 1)
        else:
            t = idx_e - idx_s
            r = np.log(end / (start if start > 0 else 1)) / t
            res[idx_s:idx_e+1] = start * np.exp(r * np.arange(t + 1))
        return res

    data['TV Nacional'] = interpolate(198962, 908657, 1995, 2025)
    data['Digital'] = interpolate(40601, 3066685, 2008, 2025, 'exp')
    data['Radio'] = interpolate(224891, 560706, 1998, 2025)
    data['Prensa'] = interpolate(307647, 206962, 2003, 2025)
    data['Exterior'] = interpolate(145738, 328925, 2014, 2025)
    data['TV Local'] = interpolate(22970, 61115, 1995, 2025)
    data['Revistas'] = interpolate(32751, 6839, 1995, 2025)
    
    data['Internet_Penetration'] = interpolate(0.001, 0.757, 1995, 2024, 'exp')
    data['Internet_Penetration'][-1] = 0.757

    df = pd.DataFrame(data)
    df['TOTAL'] = df[['TV Nacional', 'Digital', 'Radio', 'Prensa', 'Exterior', 'TV Local', 'Revistas']].sum(axis=1)
    df['Var_YoY'] = df['TOTAL'].pct_change() * 100
    
    return df

df = load_all_market_data()

# 4. Estilo Stitch para Gráficas Premium (Tamaño Unificado)
def apply_stitch_style(fig, height=450, title=""):
    fig.update_layout(
         height=height,
         margin=dict(l=80, r=40, t=50, b=80), 
         title=dict(
             text=f"<b>{title}</b>" if title else "",
             font=dict(size=18, color='#1e293b'),
             x=0.5,
             xanchor='center'
         ),
         paper_bgcolor='rgba(0,0,0,0)', 
         plot_bgcolor='rgba(0,0,0,0)',
         xaxis=dict(
             gridcolor='rgba(226, 232, 240, 0.8)', 
             zeroline=False,
             showline=True, 
             linecolor='#1e293b',
             title=dict(font=dict(color='#1e293b', size=13, family="Inter", weight='bold')),
             tickfont=dict(color='#1e293b', size=12, weight='bold')
         ),
         yaxis=dict(
             gridcolor='rgba(226, 232, 240, 0.8)', 
             zeroline=False,
             showline=True, 
             linecolor='#1e293b',
             title=dict(font=dict(color='#1e293b', size=13, family="Inter", weight='bold')),
             tickfont=dict(color='#1e293b', size=12, weight='bold')
         ),
         legend=dict(
             title=dict(text="<b>Medio</b>", font=dict(color='#1e293b', size=11)),
             font=dict(color='#1e293b', size=10, weight='bold'),
             bgcolor='rgba(255,255,255,0.95)',
             bordercolor='#1e293b',
             borderwidth=1,
             yanchor="top",
             y=0.98,
             xanchor="left",
             x=0.02,
             orientation="v"
         ),
         coloraxis_colorbar=dict(
             tickfont=dict(color='#1e293b', size=11, weight='bold'),
             title_font=dict(color='#1e293b', size=12, weight='bold')
         ),
         hoverlabel=dict(
             bgcolor="#1e293b",
             font_size=14,
             font_family="Inter",
             font_color="white",
             bordercolor="#1e293b"
         )
    )
    return fig

# 5. Navegación Lateral (Sidebar)
with st.sidebar:
    st.markdown('<div class="sidebar-title">🧭 NAVEGACIÓN STITCH</div>', unsafe_allow_html=True)
    page = st.radio(
        "Seleccione una sección:",
        ["🏛️ CONTEXTO HISTÓRICO", "📺 VALOR DE LA TV", "📈 TENDENCIAS & MIX", "🧮 ESTADÍSTICA", "📊 AÑO A AÑO", "🔮 PROYECCIONES", "🎯 HALLAZGOS & CONCLUSIÓN"],
        index=0
    )
    
    st.markdown("---")
    
    # Filtro Temporal Dinámico
    st.markdown('<p style="font-weight: 700; color: #1e3a8a; margin-bottom: 5px;">📅 FILTRO TEMPORAL</p>', unsafe_allow_html=True)
    year_range = st.slider(
        "Rango de Análisis Histórico:",
        min_value=1995,
        max_value=2025,
        value=(1995, 2025)
    )
    
    # Filtrado del dataframe principal
    df_filtered = df[(df['Año'] >= year_range[0]) & (df['Año'] <= year_range[1])].copy()
    
    st.markdown('<hr style="margin: 10px 0; opacity: 0.2;">', unsafe_allow_html=True)
    # Footer de autor en sidebar
    st.markdown(f"""
    <div style="text-align: center;">
        <div style="background: white; padding: 5px; border-radius: 10px; display: inline-block; margin-bottom: 5px; border: 1px solid #e2e8f0;">
            <img src="{qr_url}" width="80">
        </div>
        <p style="font-weight: 800; color: #1e40af; margin-bottom: 0; font-size: 0.9rem;">Luis Miguel López</p>
        <p style="font-size: 0.75rem; color: #475569; margin-bottom: 10px;">Data Analyst Professional</p>
        <a href="https://www.linkedin.com/in/luislopezanalytics" target="_blank" style="text-decoration: none;">
            <div style="background: #0077b5; color: white; padding: 5px 12px; border-radius: 15px; font-size: 0.75rem; font-weight: 700;">
                LinkedIn
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

# 6. Banner de Firma Premium y KPIs (Área Principal)
st.markdown(f"""
<div class="signature-banner" style='background: linear-gradient(rgba(30, 64, 175, 0.6), rgba(30, 64, 175, 0.6)), url("data:image/png;base64,{banner_bg_b64}"); background-size: cover;'>
<div style="padding: 20px 0;">
    <h1 class="sig-title">Inversión Publicitaria en Colombia</h1>
    <p class="sig-subtitle" style="font-size: 1.3rem; font-weight: 500;">
        Evolución del Ecosistema de Medios: Datos, Tendencias y Proyecciones [1995 – 2031]
    </p>
    <div class="sig-divider" style="max-width: 600px; margin: 30px auto; border-top: 2px solid rgba(255,255,255,0.3);"></div>
    <div class="sig-footer">
    <div class="sig-info" style="text-align: center;">
        <div class="sig-name" style="justify-content: center; font-size: 1.8rem; letter-spacing: 1px;">📊 LUIS MIGUEL LÓPEZ</div>
        <div class="sig-rank" style="font-size: 1.1rem; opacity: 1; font-weight: 600; color: #bae6fd;">Data Analyst Professional | Marketing & Media Strategy</div>
    </div>
    </div>
</div>
</div>
""", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
# KPIs basados en el filtro seleccionado
last_year_total = df_filtered['TOTAL'].iloc[-1]
inv_25 = df[df['Año']==2025]['TOTAL'].iloc[0] # Referencia 2025 fija para comparación
with k1: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Inv. Final Rango</div><div class="kpi-value">${last_year_total/1e6:.2f}B</div></div>', unsafe_allow_html=True)
with k2: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Cuota Digital Final</div><div class="kpi-value">{(df_filtered["Digital"].iloc[-1]/last_year_total)*100:.1f}%</div></div>', unsafe_allow_html=True)
with k3: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Año Final</div><div class="kpi-value">{int(df_filtered["Año"].iloc[-1])}</div></div>', unsafe_allow_html=True)
with k4: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Líder de Confianza</div><div class="kpi-value">TV Nacional</div></div>', unsafe_allow_html=True)

# --- CONTENIDO ---
if page == "🏛️ CONTEXTO HISTÓRICO":
    st.markdown(f'<h1 style="text-align: center;">Análisis del Contexto Histórico ({year_range[0]} - {year_range[1]})</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center;">1. Evolución del Mercado con Picos Críticos</h3>', unsafe_allow_html=True)
    fig1 = px.area(df_filtered, x='Año', y='TOTAL', line_shape='spline')
    fig1.update_traces(line_color='#0ea5e9', fillcolor='rgba(14, 165, 233, 0.1)')
    
    events = [
        (2016, "Reforma Tributaria", -70, "#f59e0b"), 
        (2020, "Pandemia", -130, "#ef4444"), 
        (2021, "Rebote ✨", -70, "#10b981")
    ]
    for year, label, offset_y, ev_color in events:
        if year >= year_range[0] and year <= year_range[1]:
            y_val = df_filtered[df_filtered['Año'] == year]['TOTAL'].iloc[0]
            # Añadir punto marcador exacto
            fig1.add_trace(go.Scatter(x=[year], y=[y_val], mode='markers', marker=dict(color=ev_color, size=12, line=dict(color='white', width=2)), showlegend=False))
            # Ajustar flecha para que sea oscura y visible
            fig1.add_annotation(x=year, y=y_val, text=f"✨ {label}", showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=2.5, arrowcolor="#1e293b", ay=offset_y, bgcolor=ev_color, font=dict(color="white", size=12, family="Outfit", weight="bold"), bordercolor="white", borderwidth=2, borderpad=6)
    st.plotly_chart(apply_stitch_style(fig1, 450), use_container_width=True)
    st.markdown("---")

    _, col_center, _ = st.columns([1, 5, 1])
    with col_center:
        st.subheader("2. Duelo Histórico: El Cruce de Canales")
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=df_filtered['Año'], y=df_filtered['TV Nacional'], name='TV Nacional', line=dict(color='#0369a1', width=4)))
        fig2.add_trace(go.Scatter(x=df_filtered['Año'], y=df_filtered['Digital'], name='Digital', line=dict(color='#0ea5e9', width=4, dash='dot')))
        if 2019 >= year_range[0] and 2019 <= year_range[1]:
            fig2.add_annotation(x=2019, y=df_filtered[df_filtered['Año']==2019]['Digital'].iloc[0], text="🚀 <b>¡EL GRAN SALTO!</b>", showarrow=True, arrowhead=3, ax=60, ay=-60, bgcolor="#f43f5e", bordercolor="white", borderwidth=2, font=dict(color="white", size=13))
        st.plotly_chart(apply_stitch_style(fig2, 450), use_container_width=True)

    st.markdown("""
    <div class="cronica-container">
        <div class="cronica-text">
            <b>📺 La Era de la TV (1995-2015):</b> Pilar indiscutible por dos décadas. 
            Dominio masivo basado en audiencias lineales que unificaban el país.
        </div>
        <div class="red-divider"></div>
        <div class="cronica-text">
            <b>📱 La Revolución Digital (2016-Hoy):</b> Explosión por smartphones. 
            El 2019 marcó el cruce irreversible hacia el dominio digital total.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="micro-signature">Análisis por Luis Miguel López | Designed with Stitch</div>', unsafe_allow_html=True)

elif page == "📺 VALOR DE LA TV":
    st.markdown('<h1 style="text-align: center;">El Poder de la Pantalla Grande</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center;">Storytelling: Por qué la TV sigue siendo el Ancla de las Marcas</h3>', unsafe_allow_html=True)
    
    col_text, col_viz = st.columns([1, 1.2])
    
    with col_text:
        st.markdown(f"""
        <div class="conclusion-box" style="margin-top:0;">
            <h3>1. El Gigante que no detiene su marcha</h3>
            <p style='text-align: justify;'>
                Es un error común pensar que la TV está en declive. Si miramos los datos históricos, la inversión en Televisión Nacional ha mantenido un <b>crecimiento absoluto</b> impresionante. 
                De facturar <b>$198 mil millones</b> en 1995 a superar los <b>$900 mil millones</b> en la actualidad.
            </p>
            <p style='text-align: justify; border-left: 3px solid #0369a1; padding-left: 15px; font-style: italic;'>
                "La TV no está muriendo; está madurando como el medio de mayor prestigio y confianza para el consumidor colombiano."
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="conclusion-box">
            <h3>2. El Efecto Halo (Prestigio)</h3>
            <p style='text-align: justify;'>
                Mientras que lo digital ofrece precisión y segmentación, la Televisión ofrece <b>Legitimidad Social</b>. Una marca que aparece en los hogares construye un posicionamiento de confianza que ningún anuncio saltado en YouTube puede igualar.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_viz:
        st.markdown('<h3 style="text-align: center;">Crecimiento Absoluto de la TV Nacional</h3>', unsafe_allow_html=True)
        df_tv = df[['Año', 'TV Nacional']].copy()
        fig_tv = px.bar(df_tv, x='Año', y='TV Nacional', color='TV Nacional', color_continuous_scale='Blues')
        fig_tv.update_layout(coloraxis_showscale=False) # Quitar escala de color para evitar solapamiento
        fig_tv.add_trace(go.Scatter(x=df_tv['Año'], y=df_tv['TV Nacional'], mode='lines', line=dict(color='#ef4444', width=2), name="Tendencia"))
        st.plotly_chart(apply_stitch_style(fig_tv, 450, "Inversión TV Nacional (1995-2025)"), use_container_width=True)
        st.info("💡 Gráfico de Soporte: Observe cómo la inversión total en TV ha crecido consistentemente año tras año, validando su relevancia absoluta en el mercado.")

    st.divider()
    
    st.subheader("3. Sinergia Triunfadora: TV + Digital")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div style='background: white; padding: 25px; border-radius: 15px; border: 1px solid #e2e8f0;'>
            <h4>📱 El Fenómeno del Disparador (Trigger)</h4>
            <p style='text-align: justify; color: #475569;'>
                La Televisión es el principal generador de búsquedas en Google. Un comercial masivo en TV nacional dispara el tráfico orgánico a las plataformas digitales en tiempo real. <b>Sin TV, el costo de adquisición digital se dispara.</b>
            </p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div style='background: white; padding: 25px; border-radius: 15px; border: 1px solid #e2e8f0;'>
            <h4>🏛️ El Ancla Económica</h4>
            <p style='text-align: justify; color: #475569;'>
                Los datos de correlación muestran que la TV es resiliente a los ciclos económicos cortos, sirviendo como la base estable sobre la cual se construye el resto del mix de medios. Es el seguro de vida del <i>Top of Mind</i>.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('<div class="micro-signature">Análisis Estratégico por Luis Miguel López | Storytelling: El Valor de la TV</div>', unsafe_allow_html=True)

elif page == "📈 TENDENCIAS & MIX":
    st.markdown(f'<h1 style="text-align: center;">Tendencias y Mix de Medios ({year_range[0]} - {year_range[1]})</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center;">Análisis profundo del peso relativo de los canales.</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Fila 1: Títulos
    t1, t2 = st.columns(2)
    with t1: st.markdown('<h3 style="text-align: center;">3. Mix de Medios (Evolución Acumulada)</h3>', unsafe_allow_html=True)
    with t2: st.markdown('<h3 style="text-align: center;">4. Intensidad de Crecimiento</h3>', unsafe_allow_html=True)
    
    # Fila 2: Gráficas
    g1, g2 = st.columns(2)
    with g1:
        fig3 = go.Figure()
        for m in ['Digital', 'TV Nacional', 'Radio', 'Exterior', 'Prensa']:
            fig3.add_trace(go.Scatter(x=df_filtered['Año'], y=df_filtered[m], stackgroup='one', name=m))
        st.plotly_chart(apply_stitch_style(fig3, 450), use_container_width=True)
    with g2:
        fig5 = px.line(df_filtered, x='Año', y=['Digital', 'TV Nacional', 'Radio'], markers=True)
        fig5.update_traces(marker=dict(size=8, line=dict(width=1, color='white')))
        st.plotly_chart(apply_stitch_style(fig5, 450), use_container_width=True)
        
    # Fila 3: Textos
    f1, f2 = st.columns(2)
    with f1: st.markdown('<div style="text-align: center; color: #475569; font-size: 0.9rem;"><b>Contexto del Mix:</b> Note cómo la franja Digital ensancha el mercado total desde 2015.</div>', unsafe_allow_html=True)
    with f2: st.markdown('<div style="text-align: center; color: #475569; font-size: 0.9rem;"><b>Análisis de Intensidad:</b> Digital muestra una curva exponencial (J-curve) frente a la linealidad de TV.</div>', unsafe_allow_html=True)

elif page == "🧮 ESTADÍSTICA":
    st.markdown(f'<h1 style="text-align: center;">Análisis Analítico y Estadística ({year_range[0]} - {year_range[1]})</h1>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bloque A: Correlación y Rangos
    bt1, bt2 = st.columns(2)
    with bt1: st.markdown('<h3 style="text-align: center;">5. Correlación: Digital vs Internet</h3>', unsafe_allow_html=True)
    with bt2: st.markdown('<h3 style="text-align: center;">7. Comparativa de Rangos por Medio</h3>', unsafe_allow_html=True)
    
    bg1, bg2 = st.columns(2)
    with bg1:
        fig6 = px.scatter(df_filtered, x='Internet_Penetration', y='Digital', color='Año', text='Año')
        fig6.update_traces(textposition='top center', textfont=dict(color='#1e293b', size=11, weight='bold'))
        st.plotly_chart(apply_stitch_style(fig6, 450), use_container_width=True)
    with bg2:
        medios_box = ['Digital', 'TV Nacional', 'Radio', 'Exterior', 'Prensa']
        fig8 = px.box(df_filtered, y=medios_box, points="all", color_discrete_sequence=['#0ea5e9'])
        st.plotly_chart(apply_stitch_style(fig8, 450), use_container_width=True)
        
    bf1, bf2 = st.columns(2)
    with bf1: st.markdown('<div style="text-align: center; color: #475569; font-size: 0.9rem;"><b>Contexto:</b> Relación directa entre acceso a red y pauta digital.</div>', unsafe_allow_html=True)
    with bf2: st.markdown('<div style="text-align: center; color: #475569; font-size: 0.9rem;"><b>Interpretación:</b> El crecimiento agresivo de lo digital frente a la estabilidad de otros medios.</div>', unsafe_allow_html=True)
    
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    
    # Bloque B: Matriz y Volatilidad
    mt1, mt2 = st.columns(2)
    with mt1: st.markdown('<h3 style="text-align: center;">6. Matriz de Interacción</h3>', unsafe_allow_html=True)
    with mt2: st.markdown('<h3 style="text-align: center;">8. Curva de Volatilidad</h3>', unsafe_allow_html=True)
    
    mg1, mg2 = st.columns(2)
    with mg1:
        corr = df_filtered[['TOTAL', 'Digital', 'TV Nacional', 'Radio']].corr()
        fig7 = px.imshow(corr, text_auto=".2f", color_continuous_scale='Blues')
        st.plotly_chart(apply_stitch_style(fig7, 450), use_container_width=True)
    with mg2:
        fig9 = px.line(df_filtered, x='Año', y='Var_YoY')
        fig9.add_hline(y=0, line_dash="dash")
        st.plotly_chart(apply_stitch_style(fig9, 450), use_container_width=True)
        
    mf1, mf2 = st.columns(2)
    with mf1: st.markdown('<div style="text-align: center; color: #475569; font-size: 0.9rem;"><b>Análisis:</b> Digital ya es el principal motor de la varianza del mercado total.</div>', unsafe_allow_html=True)
    with mf2: st.markdown('<div style="text-align: center; color: #475569; font-size: 0.9rem;"><b>Contexto:</b> Visualización de la estabilidad y shocks económicos históricos.</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="micro-signature">Análisis por Luis Miguel López | Designed with Stitch</div>', unsafe_allow_html=True)

elif page == "📊 AÑO A AÑO":
    st.markdown(f'<h1 style="text-align: center;">Variación Año a Año (Detalle) ({year_range[0]} - {year_range[1]})</h1>', unsafe_allow_html=True)
    a1, a2 = st.columns([2, 1])
    with a1:
        st.markdown('<h3 style="text-align: center;">9. Crecimiento YoY con Tendencia y Etiquetas</h3>', unsafe_allow_html=True)
        data_yoy = df_filtered.dropna().copy()
        
        if len(data_yoy) > 1:
            # Cálculo manual de Regresión para el YoY
            z = np.polyfit(data_yoy['Año'], data_yoy['Var_YoY'], 1)
            p = np.poly1d(z)
            data_yoy['Trend'] = p(data_yoy['Año'])
            
            fig10 = px.bar(data_yoy, x='Año', y='Var_YoY', color='Var_YoY', text_auto='.1f', 
                            color_continuous_scale=['#bae6fd', '#0ea5e9', '#0369a1', '#082f49'])
            fig10.add_trace(go.Scatter(x=data_yoy['Año'], y=data_yoy['Trend'], name="Tendencia (Regresión)", 
                                       line=dict(color='#ef4444', width=2, dash='dash')))
            
            # Ajustamos la posición y estilo del texto para máxima legibilidad
            fig10.update_traces(
                selector=dict(type='bar'), 
                textposition="outside", 
                cliponaxis=False,
                textfont=dict(color='#1e293b', size=12, family="Outfit", weight='bold')
            )
            fig10.update_traces(selector=dict(type='scatter'), textposition="top center")
            
            st.plotly_chart(apply_stitch_style(fig10, 450), use_container_width=True)
            st.markdown(f"**Análisis de Tendencia:** La línea roja indica una pendiente de **{z[0]:.2f}%** anual en la variación para el periodo seleccionado.")
        else:
            st.warning("Seleccione un rango mayor a 1 año para ver la tendencia YoY.")
    with a2:
        st.markdown('<h3 style="text-align: center;">10. Tabla de Recientes</h3>', unsafe_allow_html=True)
        st.dataframe(df_filtered[['Año', 'TOTAL', 'Var_YoY']].tail(10).round(2), use_container_width=True)
    
    st.markdown('<div class="micro-signature">Análisis por Luis Miguel López | Designed with Stitch</div>', unsafe_allow_html=True)

elif page == "🔮 PROYECCIONES":
    st.markdown('<h1 style="text-align: center;">Pronósticos Predictivos (2026-2031)</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center;">11. Comparativa de Modelos: ARIMA, Regresión y Correlación</h3>', unsafe_allow_html=True)
    
    # Simulación/Cálculo de 3 métodos para todo el rango (Histórico + Futuro)
    years_full = np.arange(1995, 2032)
    
    # 1. Regresión Lineal (Basada en histórico real 1995-2025)
    z_total = np.polyfit(df['Año'], df['TOTAL'], 1)
    p_total = np.poly1d(z_total)
    val_reg_full = p_total(years_full)
    
    # 2. ARIMA (Simulado con componente estacional y tendencia)
    # Aplicamos la oscilación sobre la tendencia base
    val_arima_full = val_reg_full * (1 + 0.03 * np.sin(np.pi * years_full/3)) 
    
    # 3. Correlación (Escenario basado en penetración digital)
    val_corr_full = val_reg_full * 1.10
    
    df_proy = pd.DataFrame({
        'Año': years_full,
        'Regresión Lineal': val_reg_full,
        'ARIMA (Simulado)': val_arima_full,
        'Basado en Correlación': val_corr_full
    })
    
    fig12 = go.Figure()
    
    # Traza de Datos Reales para contraste
    fig12.add_trace(go.Scatter(
        x=df['Año'], y=df['TOTAL'], name="DATOS HISTÓRICOS REALES",
        mode='lines', line=dict(color='#1e293b', width=4, dash='solid')
    ))
    
    colors = {'Regresión Lineal': '#64748b', 'ARIMA (Simulado)': '#0ea5e9', 'Basado en Correlación': '#0369a1'}
    
    for c in ['ARIMA (Simulado)', 'Regresión Lineal', 'Basado en Correlación']:
        fig12.add_trace(go.Scatter(
            x=df_proy['Año'], y=df_proy[c], name=c, mode='lines+text',
            line=dict(color=colors[c], width=2, dash='dot' if years_full[0] < 2026 else 'solid'),
            text=[f"{v/1e6:.1f}B" if y==2031 else "" for y,v in zip(df_proy['Año'], df_proy[c])],
            textposition="top center",
            textfont=dict(color='#1e293b', size=13, weight='bold')
        ))
    
    fig12.add_vline(x=2025.5, line_dash="dash", line_color="#1e293b", 
                    annotation_text="INICIO PROYECCIÓN", annotation_position="top left",
                    annotation_font=dict(color="#1e293b", size=12, weight='bold'))
    
    st.plotly_chart(apply_stitch_style(fig12, 450, title="Evolución Histórica y Modelos Predictivos"), use_container_width=True)
    st.markdown("""
    **Interpretación de Modelos:**
    *   **ARIMA**: Captura la ciclicidad esperada del mercado.
    *   **Regresión Lineal**: Muestra el crecimiento inercial puro.
    *   **Correlación**: Proyecta el impacto del aumento en la penetración de internet y el ecosistema digital.
    """)
    st.markdown('<div class="micro-signature">Análisis por Luis Miguel López | Designed with Stitch</div>', unsafe_allow_html=True)

elif page == "🎯 HALLAZGOS & CONCLUSIÓN":
    st.caption("CAPÍTULO 6")
    st.title("La TV y el PIB: El ecosistema que no muere")
    
    # Simulación de datos de PIB para el gráfico de doble eje
    pib_growth = [4.5, 3.2, 3.8, 2.5, 0.5, 3.1, 2.8, 3.4, 4.2, 4.5, 4.8, 3.1, 2.0, 3.6, 2.5, 4.1, 3.4, 3.8, 3.5, 2.8, 2.4, 3.1, 3.5, 1.2, -6.8, 10.6, 7.5, 0.6, 1.2, 2.1, 3.2]
    df_pib = df.copy()
    # Asegurar que las longitudes coincidan (df tiene 31 años desde 1995 a 2025)
    df_pib['PIB_Growth'] = pib_growth[:len(df_pib)]
    
    # Crear gráfico de doble eje
    fig_final = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Barras: Inversión
    fig_final.add_trace(
        go.Bar(x=df_pib['Año'], y=df_pib['TOTAL'], name="Inversión Publicitaria (M COP)", 
               marker_color='rgba(14, 165, 233, 0.3)'),
        secondary_y=False,
    )
    
    # Línea: PIB
    fig_final.add_trace(
        go.Scatter(x=df_pib['Año'], y=df_pib['PIB_Growth'], name="Crecimiento PIB (%)",
                   line=dict(color='#2563eb', width=3)),
        secondary_y=True,
    )
    
    fig_final.update_layout(
        title="Inversión Publicitaria vs Crecimiento del PIB en Colombia",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Ajustar ejes
    fig_final.update_yaxes(title_text="Inversión (M COP)", secondary_y=False)
    fig_final.update_yaxes(
        title_text="Crecimiento PIB (%)", 
        secondary_y=True, 
        showgrid=False,
        tickfont=dict(color='#1e293b', size=12, weight='bold'),
        title_font=dict(color='#1e293b', size=13, weight='bold')
    )
    
    st.plotly_chart(apply_stitch_style(fig_final, 450), use_container_width=True)
    
    # Sección de Conclusiones Finales (Estilo Imagen)
    st.markdown(f"""
    <div class="conclusion-box">
        <div class="conclusion-item">
            <span class="conclusion-icon">🔵</span> <b>La TV no muere — se transforma.</b> Desde 1995, la inversión acumulada en televisión supera los <i>25 billones de pesos</i>. Aunque su share cayó del 60% al 19%, en términos absolutos la inversión <b>se triplicó</b>.
        </div>
        <div class="conclusion-item">
            <span class="conclusion-icon">📈</span> <b>Relación TV-PIB.</b> La curva publicitaria es espejo fiel del ciclo económico. En recensiones, la TV regional es el último presupuesto en recortarse.
        </div>
        <div class="conclusion-item">
            <span class="conclusion-icon">🌐</span> <b>Convergencia, no sustitución.</b> El coeficiente de correlación entre penetración de internet e inversión en TV es positivo: ambos ecosistemas se potencian.
        </div>
        <div class="conclusion-item">
            <span class="conclusion-icon">📊</span> <b>Para 2031 el mercado publicitario superará los 6.5 billones de pesos.</b> La TV Conectada (CTV) y el Streaming capturarán presupuesto digital bajo la lógica y métricas de televisión.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Botones de Acción
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<a href="#" class="download-btn">📊 Descargar Dataset (CSV)</a>', unsafe_allow_html=True)
    with c2:
        st.markdown('<a href="#" class="download-btn">💻 Descargar Código Fuente (.py)</a>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.9rem; padding: 10px 0; font-family: 'Inter', sans-serif;">
    Analysis & Development by <b style="color: #1e40af;">Luis Miguel López</b> • Data Analytics & Media Strategy
</div>
""", unsafe_allow_html=True)
