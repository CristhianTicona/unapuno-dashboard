"""
Dashboard de ingresantes a la UNA Puno, proceso 2024-I.

Un solo scroll: portada, dataset, mapa nacional + provincial, segregación de
género por carrera, brecha escolar entre provincias. Los filtros del sidebar
solo tocan las secciones 2 y 3.
"""

import streamlit as st
import pandas as pd

from src.constants import (
    TITULO_APP, SUBTITULO_APP, TESIS,
    TITULO_SECCION_1, SUBTITULO_SECCION_1,
    TITULO_SECCION_2, SUBTITULO_SECCION_2,
    TITULO_SECCION_3, SUBTITULO_SECCION_3,
    CIERRE, FUENTE_GRAFICOS, PLOTLY_CONFIG,
)
from src.data_loader import cargar_todo
from src.charts import (
    mapa_nacional, mapa_puno, barras_externos,
    donut_proceso, barras_genero_carrera, scatter_brecha_escolar,
)


st.set_page_config(
    page_title=TITULO_APP,
    page_icon="🎓",
    layout="wide",
)


# Streamlit re-ejecuta el script en cada interacción, así que cargamos una vez
# y dejamos que st.cache_data haga el trabajo. Sin esto, cada click en un
# filtro vuelve a leer parquet + geojson y se nota.
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
# Ojo: los filtros solo afectan a las secciones 2 y 3. Los mapas se calculan
# con el dataset completo, si no cambia el color de las provincias al filtrar
# por sexo y se pierde la lectura territorial.
with st.sidebar:
    st.title("Filtros")
    st.caption("Solo afectan a las secciones 02 y 03.")

    # df["SEXO"].unique() devuelve un numpy array. Streamlit compara las
    # opciones con == en cada rerun, y con numpy eso da un array de booleanos
    # en lugar de un booleano: el widget cree que cambiaron las opciones y
    # dispara un rerun → se calcula de nuevo → loop. Con .tolist() pasa a ser
    # una lista de Python, que se compara bien.
    opciones_sexo = sorted(df["SEXO"].dropna().unique().tolist())
    sexo_sel = st.multiselect(
        "Sexo",
        options=opciones_sexo,
        default=opciones_sexo,
    )

    opciones_proceso = sorted(df["PROCESO_ADMISION"].dropna().unique().tolist())
    proceso_sel = st.multiselect(
        "Proceso de admisión",
        options=opciones_proceso,
        default=opciones_proceso,
    )

    with st.expander("Fuente y licencia"):
        st.markdown("""
        - **Fuente:** Universidad Nacional del Altiplano (datos abiertos)
        - **Licencia:** Open Data Commons Attribution
        - **Marco legal:** Ley N° 27806 (Transparencia)
        - **Periodo:** 2024-I (corte transversal)
        """)

    with st.expander("Decisiones de limpieza"):
        st.markdown("""
        - El UBIGEO del dataset no sigue el estándar INEI. Puno aparece
          con código `20` (debería ser `21`) y las provincias están
          desalineadas desde la 2105. Cruzamos con el shapefile por
          nombre, no por código.
        - Un caso de doble ingreso (mismo DNI, CEPREUNA + General).
          Nos quedamos con el puntaje más alto.
        - `TIPO_COLEGIO` venía en 5 variantes → lo dejamos en 3.
        - Un año de egreso 2029 (imposible). Queda anotado como limitación.
        """)


df_filtrado = df[
    df["SEXO"].isin(sexo_sel) & df["PROCESO_ADMISION"].isin(proceso_sel)
].copy()


# --- Portada ---
st.title(f"🎓 {TITULO_APP}")
st.caption(SUBTITULO_APP)
st.markdown(f"> **Tesis:** *{TESIS}*")
st.divider()


# --- El dataset (metadatos + muestra) ---
st.header("El dataset en números")
st.markdown(
    "Antes de la historia, los datos. Es un corte transversal del proceso "
    "2024-I: 1.890 ingresantes con 25 variables demográficas, geográficas y "
    "académicas. No hay serie temporal."
)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Registros", f"{len(df):,}")
m2.metric("Variables", df.shape[1])
m3.metric("Procesos de admisión", df["PROCESO_ADMISION"].nunique())
m4.metric("Cobertura", "13 departamentos")

col_muestra, col_resumen = st.columns([3, 2])

with col_muestra:
    st.markdown("**Algunas filas (identificadores hasheados en la fuente)**")
    muestra = df[[
        "SEXO", "DEPARTAMENTO_PROCEDENCIA", "PROVINCIA_PROCEDENCIA",
        "ESCUELA_PROFESIONAL", "TIPO_COLEGIO_NORM", "PUNTAJE",
    ]].head(8)
    st.dataframe(muestra, use_container_width=True, hide_index=True)
    st.caption(
        f"Mostramos 8 de {len(df):,} registros. Los nombres y el DNI vienen "
        "hasheados desde la fuente original."
    )

with col_resumen:
    st.markdown("**Resumen de las 25 columnas**")

    # Columnas que agregamos nosotros durante la limpieza, no las mostramos
    cols_internas = {
        "PROV_NORM", "DEPTO_NORM", "UBIGEO_DIST",
        "UBIGEO_PROV_RAW", "UBIGEO_DEP_RAW", "TIPO_COLEGIO_NORM",
    }

    mapa_tipos = {
        "object": "texto",
        "int64": "entero",
        "float64": "decimal",
    }

    metadatos = []
    for col in df.columns:
        if col in cols_internas:
            continue
        metadatos.append({
            "Variable": col if len(col) <= 25 else col[:22] + "...",
            "Tipo": mapa_tipos.get(str(df[col].dtype), str(df[col].dtype)),
            "Únicos": int(df[col].nunique()),
            "Nulos": int(df[col].isnull().sum()),
        })

    st.dataframe(
        pd.DataFrame(metadatos),
        use_container_width=True,
        hide_index=True,
        height=290,
    )

# Mini-gráfico: cómo se reparte el dataset por proceso.
# Lo dejamos acá porque es un dato de "composición", no de análisis.
st.markdown("**¿Cómo se compone el dataset por proceso de admisión?**")
st.plotly_chart(
    donut_proceso(df),
    use_container_width=True,
    config=PLOTLY_CONFIG,
)

st.caption(FUENTE_GRAFICOS)
st.divider()


# --- Sección 01: territorio ---
st.header(TITULO_SECCION_1)
st.markdown(SUBTITULO_SECCION_1)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Vista nacional")
    st.plotly_chart(
        mapa_nacional(agg_deptos, geo_deptos),
        use_container_width=True,
        config=PLOTLY_CONFIG,
    )
    st.caption(
        "El 94.8% viene de Puno. El resto es goteo del sur: Cusco, Arequipa, "
        "Lima, Tacna y otros departamentos con 1-3 casos."
    )

with col2:
    st.subheader("Zoom a las 13 provincias de Puno")
    st.plotly_chart(
        mapa_puno(agg_provincias, geo_provincias),
        use_container_width=True,
        config=PLOTLY_CONFIG,
    )
    st.caption(
        "La capital aporta 30.2%. Juliaca (San Román) 18.4%. El 51.4% restante "
        "viene de las otras 11 provincias. No es una universidad de la ciudad, "
        "es de la región."
    )

# Los 98 de fuera de Puno. Van aparte porque en el mapa se invisibilizan.
st.subheader("¿Y los que vienen de fuera de Puno?")
st.markdown(
    "Son **98 ingresantes (5.2%)** en 12 departamentos. Analizamos si tenían "
    "perfil propio y no: el puntaje medio es casi idéntico (1908 vs 1913) y el "
    "gap educativo también (3.8 vs 3.4 años). Son goteo regional, no un grupo "
    "diferenciado."
)

col_ext_graf, col_ext_datos = st.columns([2, 1])

with col_ext_graf:
    st.plotly_chart(
        barras_externos(df),
        use_container_width=True,
        config=PLOTLY_CONFIG,
    )

with col_ext_datos:
    st.markdown("**Carreras más elegidas:**")
    st.markdown("""
    - Turismo: 8 (16.3% de la carrera)
    - Ing. Mecánica Eléctrica: 5
    - Medicina Veterinaria: 5
    - Odontología: 5
    - Cs. de la Comunicación: 5
    """)
    st.markdown("**Modalidad de ingreso:**")
    st.markdown("""
    - Examen General: 56
    - CEPREUNA: 30
    - Primeros Puestos: 6
    """)

st.caption(FUENTE_GRAFICOS)
st.divider()


# --- Sección 02: género por carrera ---
st.header(TITULO_SECCION_2)
st.markdown(SUBTITULO_SECCION_2)

g1, g2, g3, g4 = st.columns(4)
g1.metric("Rango de segregación", "96 pts")
g2.metric("Más feminizada", "Ed. Inicial", "100% F")
g3.metric("Más masculinizada", "Ing. Mec. Eléctrica", "4% F")
g4.metric("Carreras", "44")

st.markdown("")
st.plotly_chart(
    barras_genero_carrera(df_filtrado),
    use_container_width=True,
    config=PLOTLY_CONFIG,
)
st.caption(
    "Cada barra va del eje central hacia el porcentaje correspondiente. "
    "La línea punteada marca el 50% (paridad)."
)
st.caption(FUENTE_GRAFICOS)
st.divider()


# --- Sección 03: brecha escolar ---
st.header(TITULO_SECCION_3)
st.markdown(SUBTITULO_SECCION_3)

st.plotly_chart(
    scatter_brecha_escolar(agg_provincias),
    use_container_width=True,
    config=PLOTLY_CONFIG,
)

st.markdown("""
**Cómo leerlo:** cada burbuja es una provincia. El tamaño es la cantidad de
ingresantes. En X, el % de colegios privados; en Y, el puntaje mediano. La
línea punteada es la tendencia lineal.

**Los casos que rompen la tendencia:**

- **Yunguyo**: casi sin colegios privados (1.6%) pero segundo mejor puntaje
  mediano (1962).
- **Moho**: mejor puntaje (1966) y 30% privado, pero solo 23 ingresantes.
- **Chucuito**: peor puntaje (1808) con 7.3% privado.

El origen escolar correlaciona con el puntaje pero no lo determina. Esa es la
idea de esta sección: la tendencia existe y tiene excepciones que pesan.
""")
st.caption(FUENTE_GRAFICOS)
st.divider()


# --- Cierre ---
st.header("Cierre")
st.markdown(f"### {CIERRE}")

st.markdown("""
**Limitaciones:**

- Corte transversal (solo 2024-I). No podemos hablar de tendencias.
- Solo tenemos ingresantes. No sabemos cuántos postularon y no entraron,
  así que no hay tasa de admisión.
- Provincias con muestra chica (Moho n=23, San Antonio de Putina n=38) tienen
  promedios volátiles.
- El UBIGEO del dataset no respeta el estándar INEI. Lo resolvimos por nombre
  pero limita la reproducibilidad técnica del cruce.
- "Pública de gestión privada" (n=19) es un híbrido que no desagregamos.
""")

st.divider()
st.caption(
    "Trabajo de Visualización de Datos · [Universidad] · Octubre 2026 · "
    "Sección 01: [Nombre 1] · Sección 02: [Nombre 2] · Sección 03: [Nombre 3]"
)
