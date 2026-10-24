"""
Dashboard de ingresantes a la UNA Puno, proceso 2024-I.
Trabajo de Visualización de Datos - Maestría en Ciencia de Datos (UNAP).
"""

import streamlit as st
import pandas as pd

from src.constants import (
    EYEBROW, TITULO_APP, SUBTITULO_APP, IDEA_CENTRAL,
    TITULO_SECCION_1, SUBTITULO_SECCION_1,
    TITULO_SECCION_2, SUBTITULO_SECCION_2,
    TITULO_SECCION_3, SUBTITULO_SECCION_3,
    CIERRE, FUENTE_GRAFICOS, PLOTLY_CONFIG,
    COLOR_FEMENINO, COLOR_MASCULINO,
)
from src.data_loader import cargar_todo
from src.charts import (
    mapa_nacional, mapa_puno, barras_externos,
    donut_proceso, barras_genero_carrera, barras_brecha_escolar,
)
from src.styles import (
    aplicar_estilos, hero, section_header, metric_card, insight_box,
    divider, footer,
)

# Configuración básica de la página
st.set_page_config(page_title=TITULO_APP, layout="wide")
aplicar_estilos()

# Cargamos los datos. Streamlit ejecuta todo de nuevo en cada interacción, 
# así que el @st.cache_data evita que se lea el parquet y el geojson de cero cada vez.
@st.cache_data(show_spinner="Cargando datos...")
def _cargar():
    return cargar_todo()

datos = _cargar()
df = datos["ingresantes"]
agg_provincias = datos["agg_provincias"]
agg_deptos = datos["agg_departamentos"]
geo_provincias = datos["geo_provincias"]
geo_deptos = datos["geo_departamentos"]

# --- Sidebar ---
with st.sidebar:
    st.title("Sobre el dashboard")
    st.markdown(
        "Este análisis se basa en los datos de los ingresantes a la Universidad "
        "Nacional del Altiplano en el proceso 2024-I."
    )
    with st.expander("Fuente y licencia", expanded=True):
        st.markdown("""
        - **Datos:** Plataforma Nacional de Datos Abiertos
        - **Entidad:** Universidad Nacional del Altiplano
        - **Licencia:** Open Data Commons Attribution
        - **Periodo:** 2024-I
        """)
    with st.expander("Notas de limpieza"):
        st.markdown("""
        - El UBIGEO original tenía errores. Puno aparecía con código `20` y las provincias estaban desalineadas. Lo arreglamos cruzando los datos con el mapa por **nombre**, no por código.
        - Había 1 caso de doble ingreso (mismo DNI). Dejamos el puntaje más alto.
        - `TIPO_COLEGIO` tenía 5 variantes distintas → las agrupamos en 3.
        """)

# --- Portada ---
hero(
    eyebrow=EYEBROW,
    titulo=TITULO_APP,
    subtitulo=SUBTITULO_APP,
    idea_central=IDEA_CENTRAL,
)

# --- El dataset en números ---
st.markdown("### El dataset en números")
st.markdown(
    "Empezamos presentando los datos. Son 1.890 ingresantes del proceso 2024-I, "
    "con 25 columnas que describen su origen, género, tipo de colegio y puntaje. "
    "Como solo tenemos este periodo, no podemos analizar tendencias en el tiempo, "
    "sino que es una foto fija de este año."
)

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    metric_card(f"{len(df):,}", "Registros")
with col_m2:
    metric_card(str(df.shape[1]), "Variables")
with col_m3:
    metric_card(str(df["PROCESO_ADMISION"].nunique()), "Procesos")
with col_m4:
    metric_card("13", "Departamentos")

st.markdown("")
col_muestra, col_resumen = st.columns([3, 2])

with col_muestra:
    st.markdown("#### Algunas filas (datos personales encriptados)")
    muestra = df[[
        "SEXO", "DEPARTAMENTO_PROCEDENCIA", "PROVINCIA_PROCEDENCIA",
        "ESCUELA_PROFESIONAL", "TIPO_COLEGIO_NORM", "PUNTAJE",
    ]].head(8)
    st.dataframe(muestra, use_container_width=True, hide_index=True, height=320)
    st.caption("Mostramos 8 de 1.890 registros. Los nombres y DNI originales vienen encriptados (hasheados) por privacidad.")

with col_resumen:
    st.markdown("#### Resumen de columnas")
    cols_internas = {"PROV_NORM", "DEPTO_NORM", "UBIGEO_DIST", "UBIGEO_PROV_RAW", "UBIGEO_DEP_RAW", "TIPO_COLEGIO_NORM"}
    mapa_tipos = {"object": "texto", "int64": "entero", "float64": "decimal"}
    
    metadatos = []
    for col in df.columns:
        if col in cols_internas: continue
        metadatos.append({
            "Variable": col if len(col) <= 22 else col[:19] + "...",
            "Tipo": mapa_tipos.get(str(df[col].dtype), str(df[col].dtype)),
            "Nulos": int(df[col].isnull().sum()),
        })
    st.dataframe(pd.DataFrame(metadatos), use_container_width=True, hide_index=True, height=320)

st.markdown("#### ¿Cómo se compone el dataset por proceso de admisión?")
_, col_donut, _ = st.columns([1, 2, 1])
with col_donut:
    st.plotly_chart(donut_proceso(df), use_container_width=True, config=PLOTLY_CONFIG)

st.caption(FUENTE_GRAFICOS)
divider()

# --- Sección 01: Territorio ---
section_header("01", TITULO_SECCION_1, SUBTITULO_SECCION_1)

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### Vista nacional")
    st.plotly_chart(mapa_nacional(agg_deptos, geo_deptos), use_container_width=True, config=PLOTLY_CONFIG)
    st.caption("El 94.8% es de Puno. El resto son casos aislados, en su mayoría de Cusco, Arequipa, Lima y Tacna.")

with col2:
    st.markdown("#### Zoom a Puno")
    st.plotly_chart(mapa_puno(agg_provincias, geo_provincias), use_container_width=True, config=PLOTLY_CONFIG)
    st.caption("La capital aporta 30.2%. Juliaca (San Román) 18.4%. El 51.4% restante viene de las otras 11 provincias.")

st.markdown("")
st.markdown("#### ¿Y los que vienen de fuera de Puno?")
st.markdown("Son **98 ingresantes (5.2%)** distribuidos en 12 departamentos. Al comparar con los de Puno, no encontramos diferencias en el puntaje promedio (1908 vs 1913) ni en la modalidad de ingreso.")

col_ext_graf, col_ext_datos = st.columns([2, 1])
with col_ext_graf:
    st.plotly_chart(barras_externos(df), use_container_width=True, config=PLOTLY_CONFIG)
with col_ext_datos:
    st.markdown("##### Carreras más elegidas (de las 98 personas):")
    st.markdown("- Turismo: 8 \n- Ing. Mecánica Eléctrica: 5\n- Medicina Veterinaria: 5\n- Odontología: 5")
    st.markdown("##### Modalidad de ingreso:")
    st.markdown("- Examen General: 56\n- CEPREUNA: 30\n- Primeros Puestos: 6")

st.caption(FUENTE_GRAFICOS)
divider()

# --- Sección 02: Género ---
section_header("02", TITULO_SECCION_2, SUBTITULO_SECCION_2)

g1, g2, g3, g4 = st.columns(4)
with g1:
    metric_card("96 pts", "Brecha de género", hint="Entre la carrera con más y menos mujeres")
with g2:
    metric_card("Ed. Inicial", "Más feminizada", hint="100% F", color=COLOR_FEMENINO)
with g3:
    metric_card("Ing. Mecánica Eléctrica", "Más masculinizada", hint="4% F", color=COLOR_MASCULINO)
with g4:
    metric_card("44", "Carreras", hint="analizadas")

st.markdown("")
st.plotly_chart(barras_genero_carrera(df), use_container_width=True, config=PLOTLY_CONFIG)
st.caption("Cada barra va del eje central hacia el porcentaje correspondiente. La línea punteada marca el 50%.")
st.caption(FUENTE_GRAFICOS)
divider()

# --- Sección 03: Brechas ---
section_header("03", TITULO_SECCION_3, SUBTITULO_SECCION_3)

st.plotly_chart(barras_brecha_escolar(agg_provincias), use_container_width=True, config=PLOTLY_CONFIG)

insight_box(
    "<strong>Cómo leerlo:</strong> el largo de la barra es el puntaje mediano de la provincia, "
    "y el color indica el % de colegios privados.<br><br>"
    "• <strong>Yunguyo</strong>: casi sin colegios privados, pero segundo mejor puntaje.<br>"
    "• <strong>Moho</strong>: mejor puntaje y 30% privado, pero solo 23 ingresantes.<br>"
    "• <strong>Chucuito</strong>: peor puntaje, con 7% privado.<br><br>"
    "El origen escolar importa, pero no marca el destino."
)

st.caption(FUENTE_GRAFICOS)
divider()

# --- Cierre ---
st.markdown("### Cierre")
st.markdown(f"> {CIERRE}")

st.markdown("**Limitaciones del análisis:**")
st.markdown("""
- Es un corte transversal (solo 2024-I). No podemos analizar tendencias.
- Solo tenemos datos de los que ingresaron. No sabemos cuántos postularon y no entraron.
- Provincias con muestra chica (Moho n=23) tienen promedios que pueden variar mucho.
- El UBIGEO del dataset no respeta el estándar INEI. Lo resolvimos por nombre.
""")

footer(
    "<strong>Visualización de Datos</strong> · Maestría en Ciencia de Datos · UNAP · 2026<br>"
    "Cristhian Ticona Cutipa · Russell Carbajal Vilca · Jean Carlos Carrasco Cutisaca"
)
