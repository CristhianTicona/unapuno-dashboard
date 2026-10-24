"""
Funciones de gráficos.

Cada función devuelve una figura de Plotly. La app las embebe con
st.plotly_chart. Se pueden probar sin Streamlit.
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.constants import (
    COLOR_TERRITORIO,
    COLOR_HALLAZGO,
    COLOR_FEMENINO,
    COLOR_MASCULINO,
    ESCALA_CALOR,
)


def mapa_nacional(agg_deptos, geo_deptos):
    # Con fitbounds el mapa queda bien encuadrado sin tocar nada a mano.
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
    fig.update_layout(
        margin=dict(l=0, r=0, t=20, b=0),
        height=460,
        coloraxis_colorbar=dict(title="Ingresantes", thickness=14, len=0.6),
    )
    return fig


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

    # Etiquetas en el centroide. Sin esto hay que pasar el mouse por cada
    # provincia para saber cuál es cuál, y en la expo eso no funciona.
    cent = geo_provincias.copy()
    cent["cx"] = cent.geometry.centroid.x
    cent["cy"] = cent.geometry.centroid.y
    cent = cent.merge(agg_provincias[["PROV_NORM", "n_ingresantes"]], on="PROV_NORM")
    for _, row in cent.iterrows():
        fig.add_annotation(
            x=row["cx"], y=row["cy"],
            text=f"<b>{row['PROV_NORM'].title()}</b><br>{int(row['n_ingresantes'])}",
            showarrow=False,
            font=dict(size=10, color="#1F2A30"),
        )

    fig.update_layout(
        margin=dict(l=0, r=0, t=20, b=0),
        height=520,
        coloraxis_colorbar=dict(title="Ingresantes", thickness=14, len=0.6),
    )
    return fig


def barras_externos(df):
    # Los 98 que no son de Puno. Son pocos pero pesan narrativamente porque
    # muestran hasta dónde llega la universidad.
    externos = df[df["DEPTO_NORM"] != "PUNO"]
    conteo = (
        externos["DEPARTAMENTO_PROCEDENCIA"]
        .value_counts()
        .reset_index()
    )
    conteo.columns = ["depto", "n"]
    conteo = conteo.sort_values("n", ascending=True)

    fig = px.bar(
        conteo,
        x="n", y="depto",
        orientation="h",
        text="n",
        color_discrete_sequence=[COLOR_TERRITORIO],
        labels={"n": "Ingresantes", "depto": ""},
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        height=380,
        margin=dict(l=0, r=40, t=10, b=20),
        plot_bgcolor="#FAFAF7",
        xaxis=dict(gridcolor="#EAE5DA", range=[0, conteo["n"].max() * 1.15]),
    )
    return fig


def donut_proceso(df):
    # Composición del dataset por proceso. Es un gráfico de metadatos, no de
    # análisis: sirve para mostrar cómo está armada la muestra.
    conteo = df["PROCESO_ADMISION"].value_counts().reset_index()
    conteo.columns = ["proceso", "n"]

    fig = px.pie(
        conteo,
        values="n", names="proceso",
        hole=0.55,
        color_discrete_sequence=[
            COLOR_TERRITORIO, COLOR_HALLAZGO, COLOR_SECUNDARIO,
        ],
    )
    fig.update_traces(
        textposition="inside",
        textinfo="label+percent",
        textfont=dict(size=11),
    )
    fig.update_layout(
        height=280,
        margin=dict(l=0, r=0, t=10, b=10),
        showlegend=False,
    )
    return fig


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

    # Masculino hacia la izquierda (negativo) para que el eje central sea
    # la línea de paridad.
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

    fig.add_vline(x=0, line_width=1, line_color="#1F2A30")
    fig.add_vline(x=50, line_width=1, line_dash="dot", line_color="#888")
    fig.add_vline(x=-50, line_width=1, line_dash="dot", line_color="#888")

    fig.update_layout(
        barmode="overlay",
        bargap=0.15,
        height=900,
        margin=dict(l=0, r=20, t=20, b=30),
        legend=dict(orientation="h", yanchor="bottom", y=1.01, x=1, xanchor="right"),
        xaxis=dict(
            title="% de ingresantes",
            tickvals=[-100, -50, 0, 50, 100],
            ticktext=["100% M", "50% M", "0", "50% F", "100% F"],
            range=[-105, 105],
        ),
        yaxis=dict(title="", tickfont=dict(size=10)),
    )
    return fig


def _acortar_carrera(nombre):
    # Los nombres de las carreras son larguísimos. Preferí hacer un diccionario
    # manual en lugar de un split automático porque vienen en formatos muy
    # distintos entre carreras y un split dejaba algunos nombres raros.
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


def scatter_brecha_escolar(agg_provincias):
    agg = agg_provincias.copy()

    # Con n directo, Puno (541) se come la escala y Moho (23) queda invisible.
    # Con raíz cuadrada se ve la diferencia pero no rompe el gráfico.
    agg["size"] = agg["n_ingresantes"].pow(0.5) * 6 + 10

    fig = px.scatter(
        agg,
        x="pct_privado",
        y="puntaje_mediano",
        size="size",
        hover_name="PROV_NORM",
        hover_data={
            "n_ingresantes": True,
            "puntaje_mediano": ":.1f",
            "pct_privado": ":.1f",
            "size": False,
        },
        color_discrete_sequence=[COLOR_TERRITORIO],
        labels={
            "pct_privado": "% de colegios privados",
            "puntaje_mediano": "Puntaje mediano",
            "n_ingresantes": "Ingresantes",
        },
    )

    # Etiquetas solo para las provincias que cuentan la historia. Las 13 a la
    # vez es ilegible.
    destacadas = ["YUNGUYO", "MOHO", "CHUCUITO", "PUNO", "SAN ROMAN"]
    for _, row in agg[agg["PROV_NORM"].isin(destacadas)].iterrows():
        color = COLOR_HALLAZGO if row["PROV_NORM"] in ("YUNGUYO", "MOHO") else "#1F2A30"
        fig.add_annotation(
            x=row["pct_privado"],
            y=row["puntaje_mediano"],
            text=f"<b>{row['PROV_NORM'].title()}</b>",
            showarrow=True,
            arrowhead=2,
            arrowcolor=color,
            ax=15, ay=-20,
            font=dict(size=11, color=color),
        )

    # Tendencia lineal. La uso solo como referencia visual, no como modelo:
    # con 13 puntos no da para predecir nada.
    coefs = np.polyfit(agg["pct_privado"], agg["puntaje_mediano"], 1)
    x_line = np.linspace(agg["pct_privado"].min(), agg["pct_privado"].max(), 50)
    fig.add_trace(go.Scatter(
        x=x_line,
        y=coefs[0] * x_line + coefs[1],
        mode="lines",
        line=dict(color=COLOR_HALLAZGO, width=2, dash="dash"),
        name="Tendencia",
        hoverinfo="skip",
    ))

    fig.update_layout(
        height=520,
        margin=dict(l=0, r=20, t=20, b=30),
        showlegend=False,
        plot_bgcolor="#FAFAF7",
        xaxis=dict(gridcolor="#EAE5DA"),
        yaxis=dict(gridcolor="#EAE5DA"),
    )
    return fig