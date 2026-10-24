"""
Constantes: paleta, rutas, textos.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

RUTA_INGRESANTES = DATA_DIR / "ingresantes_clean.parquet"
RUTA_AGG_PROVINCIAS = DATA_DIR / "agg_provincias.csv"
RUTA_AGG_DEPARTAMENTOS = DATA_DIR / "agg_departamentos.csv"
RUTA_GEO_PROVINCIAS = DATA_DIR / "provincias_puno.geojson"
RUTA_GEO_DEPARTAMENTOS = DATA_DIR / "departamentos_peru.geojson"


# Paleta base. Usamos el teal (petróleo) como color institucional y el naranja
# solo para destacar hallazgos. Así el ojo sabe dónde mirar.
COLOR_TERRITORIO = "#1C4E5C"
COLOR_HALLAZGO = "#D97B29"
COLOR_SECUNDARIO = "#6A8A3A"

COLOR_FEMENINO = "#C6517C"
COLOR_MASCULINO = "#2E5C8A"

# Escala para mapas: de transparente (sin datos) a azul petróleo (máximo).
# Usar un color sólido en vez de marrones hace que se vea más limpio y moderno.
ESCALA_CALOR = [
    [0.0, "rgba(28, 78, 92, 0)"],
    [0.4, "rgba(28, 78, 92, 0.3)"],
    [1.0, COLOR_TERRITORIO],
]


EYEBROW = "Datos abiertos · Proceso 2024-I"
TITULO_APP = "Ingresantes UNA Puno 2024-I"
SUBTITULO_APP = (
    "Un recorrido por el perfil de quienes ingresaron a la Universidad "
    "Nacional del Altiplano en el proceso 2024-I."
)

TESIS = (
    "La UNA Puno es territorialmente diversa, pero por dentro reproduce dos "
    "desigualdades: una de género en la elección de carrera (una brecha de 96 "
    "puntos porcentuales) y otra educativa que el origen escolar explica solo "
    "parcialmente."
)

TITULO_SECCION_1 = "¿De dónde vienen?"
SUBTITULO_SECCION_1 = (
    "Vista desde el Perú, la UNA Puno es un fenómeno casi exclusivamente "
    "puntano. Vista desde Puno, es una red de 13 provincias donde la capital "
    "aporta menos de un tercio."
)

TITULO_SECCION_2 = "¿Cómo se reparten?"
SUBTITULO_SECCION_2 = (
    "En el agregado, la composición por sexo es casi paritaria: 55% masculino, "
    "45% femenino. Pero por carrera la brecha es total: de 100% mujeres en "
    "Educación Inicial a 4% en Ingeniería Mecánica Eléctrica."
)

TITULO_SECCION_3 = "¿Qué explica las brechas?"
SUBTITULO_SECCION_3 = (
    "El porcentaje de colegios privados de cada provincia no sigue una regla "
    "fija respecto al puntaje mediano de sus ingresantes. Yunguyo y Moho son "
    "la prueba de que el origen escolar importa, pero no lo determina todo."
)

CIERRE = (
    "La diversidad territorial de la UNA Puno es real, pero no garantiza "
    "equidad interna: la brecha de género en la elección de carrera es total, "
    "y la diferencia educativa entre provincias no se explica solo por el tipo "
    "de colegio de origen."
)

PLOTLY_CONFIG = {"displayModeBar": False, "displaylogo": False}
FUENTE_GRAFICOS = "Fuente: Plataforma Nacional de Datos Abiertos · Elaboración propia"
