"""
Estilos visuales (CSS) para el dashboard.
"""

import streamlit as st
from src.constants import COLOR_TERRITORIO, COLOR_HALLAZGO

CSS = f"""
<style>
/* Portada principal */
.hero {{
    padding: 2rem 0 2rem 0;
    border-bottom: 1px solid rgba(128, 128, 128, 0.2);
    margin-bottom: 2rem;
}}
.hero-eyebrow {{
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: {COLOR_HALLAZGO};
    margin-bottom: 0.75rem;
}}
.hero h1 {{
    font-size: 2.75rem;
    font-weight: 700;
    line-height: 1.1;
    color: var(--text-color);
    margin: 0 0 0.75rem 0;
    letter-spacing: -0.02em;
}}
.hero-subtitle {{
    font-size: 1.1rem;
    color: var(--text-color);
    opacity: 0.8;
    max-width: 700px;
    line-height: 1.6;
    margin-bottom: 1.25rem;
}}
.hero-tesis {{
    background-color: rgba(128, 128, 128, 0.05);
    border-left: 4px solid {COLOR_TERRITORIO};
    padding: 1rem 1.25rem;
    font-size: 0.95rem;
    color: var(--text-color);
    line-height: 1.65;
    max-width: 900px;
    border-radius: 0 6px 6px 0;
}}
.hero-tesis strong {{
    color: var(--text-color);
    opacity: 0.6;
    text-transform: uppercase;
    font-size: 0.75rem;
    letter-spacing: 0.1em;
}}

/* Títulos de las secciones (01, 02, 03) */
.section-header {{
    display: flex;
    align-items: flex-start;
    gap: 1.25rem;
    margin: 1rem 0 1.5rem 0;
}}
.section-number {{
    font-size: 2.5rem;
    font-weight: 700;
    color: {COLOR_HALLAZGO};
    line-height: 1;
    opacity: 0.9;
    min-width: 3rem;
}}
.section-text {{
    flex: 1;
    padding-top: 0.25rem;
}}
.section-text h2 {{
    font-size: 1.65rem;
    font-weight: 700;
    color: var(--text-color);
    margin: 0 0 0.4rem 0;
    letter-spacing: -0.01em;
}}
.section-text p {{
    font-size: 0.98rem;
    color: var(--text-color);
    opacity: 0.8;
    line-height: 1.65;
    margin: 0;
    max-width: 850px;
}}

/* Tarjetas de métricas */
.metric-card {{
    background-color: rgba(128, 128, 128, 0.05);
    border: 1px solid rgba(128, 128, 128, 0.15);
    border-radius: 8px;
    padding: 1.1rem 1.25rem;
    min-height: 105px;
    transition: border-color 0.2s ease;
}}
.metric-card:hover {{
    border-color: {COLOR_TERRITORIO};
}}
.metric-value {{
    font-size: 1.85rem;
    font-weight: 700;
    line-height: 1.15;
    letter-spacing: -0.02em;
    overflow-wrap: break-word;
}}
.metric-label {{
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--text-color);
    opacity: 0.6;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.35rem;
}}
.metric-hint {{
    font-size: 0.78rem;
    color: var(--text-color);
    opacity: 0.4;
    margin-top: 0.3rem;
    font-style: italic;
}}

/* Caja para resaltar hallazgos */
.insight-box {{
    background-color: rgba(217, 123, 41, 0.08);
    border-left: 4px solid {COLOR_HALLAZGO};
    padding: 1rem 1.25rem;
    border-radius: 0 6px 6px 0;
    font-size: 0.95rem;
    color: var(--text-color);
    line-height: 1.7;
    margin: 1.5rem 0 0 0;
}}

/* Separadores */
.divider {{
    height: 1px;
    background-color: rgba(128, 128, 128, 0.2);
    margin: 3rem 0 2rem 0;
}}

/* Ajustes de layout de Streamlit */
.block-container {{
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 1180px !important;
}}
[data-testid="stDataFrame"] {{
    border: 1px solid rgba(128, 128, 128, 0.2);
    border-radius: 8px;
    overflow: hidden;
}}
.js-plotly-plot .plotly .modebar {{
    display: none !important;
}}

/* Footer */
.footer {{
    border-top: 1px solid rgba(128, 128, 128, 0.2);
    padding-top: 1.5rem;
    margin-top: 3rem;
    font-size: 0.85rem;
    color: var(--text-color);
    opacity: 0.6;
    text-align: center;
    line-height: 1.8;
}}
.footer strong {{
    color: var(--text-color);
}}
</style>
"""

def aplicar_estilos():
    st.markdown(CSS, unsafe_allow_html=True)

def hero(eyebrow, titulo, subtitulo, idea_central):
    st.markdown(f"""
        <div class="hero">
            <div class="hero-eyebrow">{eyebrow}</div>
            <h1>{titulo}</h1>
            <p class="hero-subtitle">{subtitulo}</p>
            <div class="hero-tesis"><strong>Idea central · </strong>{idea_central}</div>
        </div>
    """, unsafe_allow_html=True)

def section_header(numero, titulo, subtitulo):
    st.markdown(f"""
        <div class="section-header">
            <div class="section-number">{numero}</div>
            <div class="section-text">
                <h2>{titulo}</h2>
                <p>{subtitulo}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

def metric_card(valor, etiqueta, hint=None, color=None):
    color_style = f"color: {color};" if color else ""
    hint_html = f'<div class="metric-hint">{hint}</div>' if hint else ""
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="{color_style}">{valor}</div>
            <div class="metric-label">{etiqueta}</div>
            {hint_html}
        </div>
    """, unsafe_allow_html=True)

def insight_box(texto_html):
    st.markdown(f'<div class="insight-box">{texto_html}</div>', unsafe_allow_html=True)

def divider():
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

def footer(texto_html):
    st.markdown(f'<div class="footer">{texto_html}</div>', unsafe_allow_html=True)
