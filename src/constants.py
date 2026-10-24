"""
Constantes: paleta, rutas, textos.
"""

from pathlib import Path

# Rutas relativas para que funcione igual en local o en la nube
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

RUTA_INGRESANTES = DATA_DIR / "ingresantes_clean.parquet"
RUTA_AGG_PROVINCIAS = DATA_DIR / "agg_provincias.csv"
RUTA_AGG_DEPARTAMENTOS = DATA_DIR / "agg_departamentos.csv"
RUTA_GEO_PROVINCIAS = DATA_DIR / "provincias_puno.geojson"
RUTA_GEO_DEPARTAMENTOS = DATA_DIR / "departamentos_peru.geojson"

# Paleta de colores. 
COLOR_TERRITORIO = "#1C4E5C"     # Azul petróleo
COLOR_HALLAZGO = "#D97B29"       # Naranja quemado
COLOR_SECUNDARIO = "#6A8A3A"     # Verde andino
COLOR_FEMENINO = "#C6517C"       # Magenta
COLOR_MASCULINO = "#2E5C8A"      # Azul acero

# Escala para los mapas (de gris claro a azul petróleo)
ESCALA_CALOR = [
    [0.0, "#D1D5DB"],
    [0.1, "#9CA3AF"],
    [0.4, "#60A5FA"],
    [1.0, COLOR_TERRITORIO],
]

# Textos de la interfaz
EYEBROW = "Datos abiertos · Proceso 2024-I"
TITULO_APP = "Ingresantes UNA Puno 2024-I"
SUBTITULO_APP = (
    "Un recorrido por el perfil de quienes ingresaron a la Universidad "
    "Nacional del Altiplano en el proceso 2024-I."
)

IDEA_CENTRAL = (
    "La UNA Puno recibe estudiantes de toda la región, pero dentro de la "
    "universidad se ven dos diferencias claras: una brecha de género en la "
    "elección de carrera, y otra educativa que no se explica solo por el colegio de origen."
)

TITULO_SECCION_1 = "¿De dónde vienen?"
SUBTITULO_SECCION_1 = (
    "Vista desde el Perú, la UNA Puno es un fenómeno casi exclusivamente "
    "puntano. Vista desde Puno, es una red de 13 provincias donde la capital "
    "aporta menos de un tercio."
)

TITULO_SECCION_2 = "¿Cómo se reparten?"
SUBTITULO_SECCION_2 = (
    "En el total, la proporción es casi paritaria: 55% hombres y 45% mujeres. "
    "Pero al mirar por carrera, la diferencia es total: desde 100% de mujeres "
    "en Educación Inicial hasta 4% en Ingeniería Mecánica Eléctrica."
)

TITULO_SECCION_3 = "¿Qué explica las brechas?"
SUBTITULO_SECCION_3 = (
    "El porcentaje de colegios privados de cada provincia no sigue una regla "
    "fija respecto al puntaje mediano. Yunguyo y Moho demuestran que el origen "
    "escolar importa, pero no lo define todo."
)

CIERRE = (
    "La diversidad territorial de la UNA Puno es real, pero no garantiza "
    "equidad interna: la brecha de género en la elección de carrera es total, "
    "y la diferencia educativa entre provincias no se explica solo por el tipo "
    "de colegio de origen."
)

PLOTLY_CONFIG = {"displayModeBar": False, "displaylogo": False}
FUENTE_GRAFICOS = "Fuente: Plataforma Nacional de Datos Abiertos · Elaboración propia"
