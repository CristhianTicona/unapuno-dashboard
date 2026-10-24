"""
Carga de datos.
Todas las rutas son relativas (Path(__file__)), así funciona igual en local,
en GitHub y en Streamlit Cloud. No hay rutas de Colab.
"""

import unicodedata
import pandas as pd
import geopandas as gpd

from src.constants import (
    RUTA_INGRESANTES,
    RUTA_GEO_PROVINCIAS,
    RUTA_GEO_DEPARTAMENTOS,
    RUTA_AGG_PROVINCIAS,
    RUTA_AGG_DEPARTAMENTOS,
)


def normalizar_nombre(s):
    # Mayúsculas, sin tildes, espacios colapsados. Sirve para cruzar nombres
    # entre el dataset y el shapefile cuando los códigos no son confiables
    # (que es exactamente nuestro caso).
    if pd.isna(s):
        return ""
    s = str(s).upper().strip()
    s = "".join(c for c in unicodedata.normalize("NFD", s)
                if unicodedata.category(c) != "Mn")
    return " ".join(s.split())


# Sin decoradores de caché acá. El caché se maneja un nivel arriba, en app.py
# con @st.cache_data. Tener ambos al mismo tiempo puede generar reruns.
def cargar_ingresantes():
    df = pd.read_parquet(RUTA_INGRESANTES)
    if "PROV_NORM" not in df.columns:
        df["PROV_NORM"] = df["PROVINCIA_PROCEDENCIA"].apply(normalizar_nombre)
    if "DEPTO_NORM" not in df.columns:
        df["DEPTO_NORM"] = df["DEPARTAMENTO_PROCEDENCIA"].apply(normalizar_nombre)
    return df


def cargar_agg_provincias():
    return pd.read_csv(RUTA_AGG_PROVINCIAS)


def cargar_agg_departamentos():
    return pd.read_csv(RUTA_AGG_DEPARTAMENTOS)


def cargar_geo_provincias():
    return gpd.read_file(RUTA_GEO_PROVINCIAS)


def cargar_geo_departamentos():
    return gpd.read_file(RUTA_GEO_DEPARTAMENTOS)


def cargar_todo():
    return {
        "ingresantes": cargar_ingresantes(),
        "agg_provincias": cargar_agg_provincias(),
        "agg_departamentos": cargar_agg_departamentos(),
        "geo_provincias": cargar_geo_provincias(),
        "geo_departamentos": cargar_geo_departamentos(),
    }
