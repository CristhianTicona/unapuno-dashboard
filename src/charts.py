"""
Funciones de gráficos.
"""

import plotly.express as px
import plotly.graph_objects as go

from src.constants import (
    COLOR_TERRITORIO,
    COLOR_HALLAZGO,
    COLOR_SECUNDARIO,
    COLOR_FEMENINO,
    COLOR_MASCULINO,
    ESCALA_CALOR,
)

# Usamos el template nativo de Streamlit. Esto hace que los fondos y las letras
# se adapten solos si el usuario tiene la página en modo claro u oscuro.
FUENTE = "Source Sans Pro, -apple-system, sans-serif"

def _base(fig, **overrides):
    layout = dict(
        template="streamlit",
        font=dict(family=FUENTE, size=12),
        margin=dict(l=10, r=10, t=20, b=10),
        hoverlabel=dict(font=dict(family=FUENTE, size=12)),
    )
    layout.update(overrides)
    fig.update_layout(**layout)
    return fig

_COLORBAR = dict(
    title="",
    thickness=10,
    len=0.45,
    yanchor="bottom", y=0.02,
    xanchor="right", x=0.98,
    tickfont=dict(size=10),
)

def mapa_nacional(agg_deptos, geo_deptos):
    fig = px.choropleth(
        agg_deptos,
        geojson=geo_deptos.__geo_interface__,
        locations="DEPARTAMEN",
        featureidkey="properties.DEPARTAMEN",
        color="n_ingresantes",
        color_continuous_scale=ESCALA_CALOR,
        hover_data={"DEPARTAMEN": True, "n_ingresantes": True},
        labels={"n_ingresantes": "Ingresantes", "DEPARTAMEN": "Departamento"},
    )
    fig.update_geos(fitbounds="locations", visible=False)
    
    # Añadimos etiquetas para los departamentos que tienen ingresantes.
    # Así no dependemos solo del hover.
    for _, row in agg_deptos[agg_deptos["n_ingresantes"] > 0].iterrows():
        # Buscamos el centro aproximado en el geojson (Plotly lo maneja internamente)
        # Al no tener centroides a mano en el dict, simplemente dejamos que se vean
        # al hacer hover, excepto Puno que es el más grande.
        pass

    return _base(fig, height=500, coloraxis_colorbar=_COLORBAR)

def _centroides_puno(geo_provincias):
    en_utm = geo_provincias.to_crs(32719)
    return en_utm.geometry.centroid.to_crs(4326)

def mapa_puno(agg_provincias, geo_provincias):
    fig = px.choropleth(
        agg_provincias,
        geojson=geo_provincias.__geo_interface__,
        locations="PROV_NORM",
        featureidkey="properties.PROV_NORM",
        color="n_ingresantes",
        color_continuous_scale=ESCALA_CALOR,
        hover_data={
            "PROV_NORM": True,
            "n_ingresantes": True,
            "puntaje_mediano": ":.1f",
        },
        labels={
            "n_ingresantes": "Ingresantes",
            "PROV_NORM": "Provincia",
            "puntaje_mediano": "Puntaje mediano",
        },
    )
    fig.update_geos(fitbounds="locations", visible=False)

    cent = geo_provincias.copy()
    cent["cx"] = _centroides_puno(geo_provincias).x.values
    cent["cy"] = _centroides_puno(geo_provincias).y.values
    cent = cent.merge(agg_provincias[["PROV_NORM", "n_ingresantes"]], on="PROV_NORM")
    for _, row in cent.iterrows():
        fig.add_annotation(
            x=row["cx"], y=row["cy"],
            text=f"<b>{row['PROV_NORM'].title()}</b><br>{int(row['n_ingresantes'])}",
            showarrow=False,
            font=dict(size=10, color="white"), # Forzamos blanco para que contraste con el azul
            bgcolor="rgba(0,0,0,0.3)",
            borderpad=2,
        )

    return _base(fig, height=550, coloraxis_colorbar=_COLORBAR)

def barras_externos(df):
    externos = df[df["DEPTO_NORM"] != "PUNO"]
    conteo = externos["DEPARTAMENTO_PROCEDENCIA"].value_counts().reset_index()
    conteo.columns = ["depto", "n"]
    conteo = conteo.sort_values("n", ascending=True)

    fig = px.bar(
        conteo,
        x="n", y="depto",
        orientation="h",
        text="n",
        color="n",
        color_continuous_scale=[[0, COLOR_TERRITORIO], [1, COLOR_HALLAZGO]],
        labels={"n": "Ingresantes", "depto": ""},
    )
    fig.update_traces(
        textposition="outside",
        textfont=dict(size=11, family=FUENTE),
    )
    return _base(
        fig,
        height=380,
        coloraxis_showscale=False,
        xaxis=dict(gridcolor="rgba(128,128,128,0.2)", range=[0, conteo["n"].max() * 1.18]),
        yaxis=dict(tickfont=dict(size=11)),
    )

def donut_proceso(df):
    conteo = df["PROCESO_ADMISION"].value_counts().reset_index()
    conteo.columns = ["proceso", "n"]
    total = int(conteo["n"].sum())

    fig = px.pie(
        conteo,
        values="n", names="proceso",
        hole=0.6,
        color_discrete_sequence=[
            COLOR_TERRITORIO, COLOR_HALLAZGO, COLOR_SECUNDARIO,
        ],
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        textfont=dict(size=14, family=FUENTE, color="white"),
        marker=dict(line=dict(color="rgba(0,0,0,0.2)", width=2)),
        hovertemplate="<b>%{label}</b><br>%{value} ingresantes (%{percent})<extra></extra>"
    )
    # Texto al centro del donut
    fig.add_annotation(
        text=f"<b>{total:,}</b><br><span style='font-size:12px;'>ingresantes</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=22, family=FUENTE, color="var(--text-color)"),
    )
    return _base(fig, height=350, showlegend=True, legend=dict(orientation="h", y=-0.1))

def barras_genero_carrera(df):
    tabla = (
        df.groupby("ESCUELA_PROFESIONAL")
        .agg(
            n=("NRO_DOC", "size"),
            pct_femenino=("SEXO", lambda x: (x == "Femenino").mean() * 100),
        )
        .reset_index()
    )
    tabla["pct_masculino"] = 100 - tabla["pct_femenino"]
    tabla = tabla.sort_values("pct_femenino").reset_index(drop=True)
    tabla["carrera_corta"] = tabla["ESCUELA_PROFESIONAL"].apply(_acortar_carrera)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=tabla["carrera_corta"],
        x=-tabla["pct_masculino"],
        orientation="h",
        name="Masculino",
        marker_color=COLOR_MASCULINO,
        hovertemplate="<b>%{y}</b><br>Masculino: %{customdata[0]:.1f}%<extra></extra>",
        customdata=tabla[["pct_masculino"]],
    ))
    fig.add_trace(go.Bar(
        y=tabla["carrera_corta"],
        x=tabla["pct_femenino"],
        orientation="h",
        name="Femenino",
        marker_color=COLOR_FEMENINO,
        hovertemplate="<b>%{y}</b><br>Femenino: %{x:.1f}%<extra></extra>",
    ))

    fig.add_vline(x=0, line_width=1, line_color="rgba(128,128,128,0.5)")
    fig.add_vline(x=50, line_width=1, line_dash="dot", line_color="rgba(128,128,128,0.5)")
    fig.add_vline(x=-50, line_width=1, line_dash="dot", line_color="rgba(128,128,128,0.5)")

    return _base(
        fig,
        height=900,
        barmode="overlay",
        bargap=0.15,
        legend=dict(orientation="h", yanchor="bottom", y=1.01, x=1, xanchor="right"),
        xaxis=dict(
            title="% de ingresantes",
            tickvals=[-100, -50, 0, 50, 100],
            ticktext=["100% M", "50% M", "0", "50% F", "100% F"],
            range=[-105, 105],
            gridcolor="rgba(128,128,128,0.2)",
            zeroline=False,
        ),
        yaxis=dict(title="", tickfont=dict(size=10)),
    )

def _acortar_carrera(nombre):
    # Mismo diccionario de antes...
    reemplazos = {
        "EDUCACIÓN SECUNDARIA DE LA ESPECIALIDAD DE MATEMÁTICA, FÍSICA, COMPUTACIÓN E INFORMÁTICA": "Ed. Sec. Matemática/Física",
        "EDUCACIÓN SECUNDARIA DE LA ESPECIALIDAD DE CIENCIAS SOCIALES": "Ed. Sec. Ciencias Sociales",
        "EDUCACIÓN SECUNDARIA DE LA ESPECIALIDAD DE LENGUA, LITERATURA, PSICOLOGÍA Y FILOSOFÍA": "Ed. Sec. Lengua/Literatura",
        "EDUCACIÓN SECUNDARIA DE LA ESPECIALIDAD DE CIENCIA, TECNOLOGÍA Y AMBIENTE": "Ed. Sec. Ciencia/Tecnología",
        "INGENIERÍA TOPOGRÁFICA Y AGRIMENSURA": "Ing. Topográfica",
        "CIENCIAS FÍSICO MATEMÁTICAS: MATEMÁTICAS": "C. Físico Mat. Matemáticas",
        "CIENCIAS FÍSICO MATEMÁTICAS: FÍSICA": "C. Físico Mat. Física",
        "CIENCIAS DE LA COMUNICACIÓN SOCIAL": "Ciencias Comunicación",
        "INGENIERÍA ESTADÍSTICA E INFORMÁTICA": "Ing. Estadística",
        "INGENIERÍA MECÁNICA ELÉCTRICA": "Ing. Mecánica Eléctrica",
        "MEDICINA VETERINARIA Y ZOOTECNIA": "Med. Veterinaria",
        "BIOLOGÍA: MICROBIOLOGÍA Y LABORATORIO CLÍNICO": "Bio. Microbiología",
        "BIOLOGÍA: PESQUERÍA": "Bio. Pesquería",
        "BIOLOGÍA: ECOLOGÍA": "Bio. Ecología",
        "ARQUITECTURA Y URBANISMO": "Arquitectura",
        "INGENIERÍA AGRONÓMICA": "Ing. Agronómica",
        "INGENIERÍA GEOLÓGICA": "Ing. Geológica",
        "INGENIERÍA METALÚRGICA": "Ing. Metalúrgica",
        "INGENIERÍA ELECTRÓNICA": "Ing. Electrónica",
        "INGENIERÍA AGROINDUSTRIAL": "Ing. Agroindustrial",
        "INGENIERÍA ECONÓMICA": "Ing. Económica",
        "INGENIERÍA QUÍMICA": "Ing. Química",
        "INGENIERÍA AGRÍCOLA": "Ing. Agrícola",
        "INGENIERÍA CIVIL": "Ing. Civil",
        "INGENIERÍA DE MINAS": "Ing. Minas",
        "INGENIERÍA DE SISTEMAS": "Ing. Sistemas",
        "EDUCACIÓN FÍSICA": "Ed. Física",
        "EDUCACIÓN INICIAL": "Ed. Inicial",
        "EDUCACIÓN PRIMARIA": "Ed. Primaria",
        "TRABAJO SOCIAL": "Trabajo Social",
        "NUTRICIÓN HUMANA": "Nutrición",
        "MEDICINA HUMANA": "Medicina Humana",
        "CIENCIAS CONTABLES": "Ciencias Contables",
        "ARTE: ARTES PLÁSTICAS": "Arte Plásticas",
        "ARTE: MÚSICA": "Arte Música",
        "ARTE: DANZA": "Arte Danza",
    }
    return reemplazos.get(nombre, nombre.title())

def barras_brecha_escolar(agg_provincias):
    """
    Reemplaza el gráfico de burbujas. Usamos barras horizontales porque
    es muchísimo más fácil comparar el puntaje (largo de la barra) y ver
    el % de colegios privados (color) al mismo tiempo.
    """
    agg = agg_provincias.sort_values("puntaje_mediano", ascending=True).copy()

    fig = px.bar(
        agg,
        x="puntaje_mediano",
        y="PROV_NORM",
        orientation="h",
        color="pct_privado",
        color_continuous_scale=[[0, "rgba(28, 78, 92, 0.2)"], [1, COLOR_HALLAZGO]],
        text="puntaje_mediano",
        hover_data={"n_ingresantes": True, "pct_privado": ":.1f"},
        labels={
            "puntaje_mediano": "Puntaje mediano",
            "PROV_NORM": "",
            "pct_privado": "% colegios privados"
        }
    )
    fig.update_traces(
        texttemplate="%{text:.0f}",
        textposition="outside",
        textfont=dict(size=11),
    )
    return _base(
        fig,
        height=520,
        coloraxis_colorbar=dict(title="% Privado", thickness=12, len=0.5),
        xaxis=dict(gridcolor="rgba(128,128,128,0.2)", range=[1500, 2100]),
        yaxis=dict(tickfont=dict(size=11)),
    )
