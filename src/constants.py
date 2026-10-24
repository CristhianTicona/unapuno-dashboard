"""
Constantes: paleta, rutas, textos.

Si hay que cambiar un color se cambia acá y se propaga. Los textos están
fuera de app.py para que el hilo narrativo no se descuide al editar la vista.
"""

from pathlib import Path

# Path(__file__) resuelve al directorio del archivo. Como constants.py está
# en src/, parent.parent es la raíz del repo. Funciona igual en local, en
# GitHub y en Streamlit Cloud.
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

RUTA_INGRESANTES = DATA_DIR / "ingresantes_clean.parquet"
RUTA_AGG_PROVINCIAS = DATA_DIR / "agg_provincias.csv"
RUTA_AGG_DEPARTAMENTOS = DATA_DIR / "agg_departamentos.csv"
RUTA_GEO_PROVINCIAS = DATA_DIR / "provincias_puno.geojson"
RUTA_GEO_DEPARTAMENTOS = DATA_DIR / "departamentos_peru.geojson"


# Paleta. Reservamos el naranja para los hallazgos (Yunguyo, Moho). Si se usa
# en todos lados, deja de destacar.
COLOR_TERRITORIO = "#1C4E5C"     # azul petróleo
COLOR_HALLAZGO = "#D97B29"       # naranja quemado
COLOR_NEUTRAL = "#D9D2C5"        # gris arena
COLOR_SECUNDARIO = "#6A8A3A"     # verde andino

COLOR_FEMENINO = "#C6517C"
COLOR_MASCULINO = "#2E5C8A"

ESCALA_CALOR = [
    [0.0, "#FAF6EC"],
    [0.3, "#F1D89C"],
    [0.6, "#D97B29"],
    [1.0, "#7A3D0F"],
]


TITULO_APP = "Ingresantes UNA Puno 2024-I"
SUBTITULO_APP = "Un análisis narrativo de 1.890 trayectorias"

TESIS = (
    "La UNA Puno es territorialmente diversa, pero por dentro reproduce dos "
    "desigualdades: una de género en la elección de carrera (96 puntos de "
    "rango) y otra educativa que el origen escolar solo explica parcialmente."
)

TITULO_SECCION_1 = "01 · ¿De dónde vienen?"
SUBTITULO_SECCION_1 = (
    "Vista desde el Perú, la UNA Puno es un fenómeno casi exclusivamente "
    "puntano. Vista desde Puno, es una red de 13 provincias donde la capital "
    "aporta menos de un tercio."
)

TITULO_SECCION_2 = "02 · ¿Cómo se reparten?"
SUBTITULO_SECCION_2 = (
    "En el agregado, la composición por sexo es casi paritaria: 55% masculino, "
    "45% femenino. Pero por carrera la segregación es total: de 100% mujeres "
    "en Educación Inicial a 4% en Ingeniería Mecánica Eléctrica."
)

TITULO_SECCION_3 = "03 · ¿Qué explica las brechas?"
SUBTITULO_SECCION_3 = (
    "El porcentaje de colegios privados de cada provincia correlaciona con el "
    "puntaje mediano de sus ingresantes, pero no de forma determinista. "
    "Yunguyo y Moho rompen la regla."
)

CIERRE = (
    "La diversidad territorial de la UNA Puno es real, pero no garantiza "
    "equidad interna: la segregación de género en la elección de carrera es "
    "total, y la brecha educativa entre provincias no se explica solo por el "
    "tipo de colegio de origen."
)

PLOTLY_CONFIG = {"displayModeBar": False, "displaylogo": False}

FUENTE_GRAFICOS = "Fuente: UNA Puno (datos abiertos) · Elaboración propia"
