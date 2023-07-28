from datetime import datetime, timedelta, timezone
from sys import stdout

import geopandas as gpd
import pandas as pd
import plotly.graph_objects as go
from plotly import express as px
from plotly.subplots import make_subplots

s3_directory_path = "s3://painelcovid2023/data"
if __debug__:
    macro_dados = pd.read_csv(f"{s3_directory_path}/df_dados_macro_regioes_ceara.csv")
    macro_dados_ba = pd.read_csv(f"{s3_directory_path}/df_dados_macro_regioes_bahia.csv")
else:
    # macro_dados = pd.read_csv(
    #     "https://raw.githubusercontent.com/painelcovid19/painelcovid19.github.io/main/data/df_dados_macro_regioes_ceara.csv"
    # )
    # macro_dados_ba = pd.read_csv(
    #     'https://raw.githubusercontent.com/painelcovid19/painelcovid19.github.io/main/data/df_dados_macro_regioes_bahia.csv'
    # )
    pass


# MODIFICANDO O NOME DAS COLUNAS last_available_confirmed_per_100k_inhabitants E last_available_deaths_per_100k_inhabitants
macro_dados = macro_dados.rename(
    columns={
        "last_available_confirmed_per_100k_inhabitants": "Confirmados por 100 mil habitantes",
        "last_available_deaths_per_100k_inhabitants": "Mortes por 100 mil habitantes",
    }
)

# IMPORTANDO SHAPEFILES DO CEARÁ E BAHIA
municipios_CE = gpd.read_file("shapefiles/CE_Municipios_2020.shp")
# MESCLANDO SHAPEFILE E DATASET DOS MUNICÍPIOS
macro_mapa_ceara = municipios_CE.merge(
    macro_dados, left_on="NM_MUN", right_on="city", suffixes=("", "_y")
).set_index("city")

macro_fig_ce = px.choropleth_mapbox(
    macro_mapa_ceara,
    geojson=macro_mapa_ceara.geometry,
    locations=macro_mapa_ceara.index,
    color="Confirmados por 100 mil habitantes",
    center={"lat": -4.1718, "lon": -38.7491},
    opacity=0.7,
    mapbox_style="carto-positron",
    title="Casos confirmados por 100 mil habitantes nos municípios vizinhos aos campi da Unilab no Ceará",
    labels={"Confirmados por 100 mil habitantes": ""},
    color_continuous_scale=px.colors.sequential.PuBuGn,
    zoom=7.85,
    height=600,
    width=1000,
)

macro_fig_ce_ob = px.choropleth_mapbox(
    macro_mapa_ceara,
    geojson=macro_mapa_ceara.geometry,
    locations=macro_mapa_ceara.index,
    color="Mortes por 100 mil habitantes",
    center={"lat": -4.1718, "lon": -38.7491},
    opacity=0.7,
    mapbox_style="carto-positron",
    title="Óbitos confirmados por 100 mil habitantes nos municípios vizinhos aos campi da Unilab no Ceará",
    labels={"Mortes por 100 mil habitantes": ""},
    color_continuous_scale=px.colors.sequential.PuBuGn,
    zoom=7.85,
    height=600,
    width=1000,
)

macro_dados_ba = macro_dados_ba.rename(
    columns={
        "last_available_confirmed_per_100k_inhabitants": "Confirmados por 100 mil habitantes",
        "last_available_deaths_per_100k_inhabitants": "Mortes por 100 mil habitantes",
    }
)

municipios_BA = gpd.read_file("shapefiles/BA_Municipios_2020.shp")

macro_mapa_bahia = municipios_BA.merge(
    macro_dados_ba, left_on="NM_MUN", right_on="city", suffixes=("", "_y")
).set_index("city")

macro_fig_ba = px.choropleth_mapbox(
    macro_mapa_bahia,
    geojson=macro_mapa_bahia.geometry,
    locations=macro_mapa_bahia.index,
    color="Confirmados por 100 mil habitantes",
    center={"lat": -12.6089, "lon": -38.654},
    opacity=0.7,
    mapbox_style="carto-positron",
    title="Casos confirmados por 100 mil habitantes nos municípios vizinhos ao campus da Unilab na Bahia",
    labels={"Confirmados por 100 mil habitantes": ""},
    color_continuous_scale=px.colors.sequential.PuBuGn,
    zoom=7.85,
    height=600,
    width=1000,
)

macro_fig_ba_ob = px.choropleth_mapbox(
    macro_mapa_bahia,
    geojson=macro_mapa_bahia.geometry,
    locations=macro_mapa_bahia.index,
    color="Mortes por 100 mil habitantes",
    center={"lat": -12.6089, "lon": -38.654},
    opacity=0.7,
    mapbox_style="carto-positron",
    title="Óbitos confirmados por 100 mil habitantes nos municípios vizinhos ao campus da Unilab na Bahia",
    labels={"Mortes por 100 mil habitantes": ""},
    color_continuous_scale=px.colors.sequential.PuBuGn,
    zoom=7.85,
    height=600,
    width=1000,
)

macro_fig_ba_ob.write_html("teste.html")


