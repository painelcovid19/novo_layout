from datetime import datetime, timedelta, timezone
import geopandas as gpd
import pandas as pd
from plotly import express as px
from plotly import express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


if __debug__:
    df_cidades_campi = pd.read_csv("./data/df_cidades_campi.csv")
    df_mapas = pd.read_csv("./data/df_dados_acumulados.csv")
    df_atualizacao = pd.read_csv("./data/last_update_dates.csv")
else:
    df_cidades_campi = pd.read_csv(
        "https://raw.githubusercontent.com/painelcovid19/painelcovid19.github.io/main/data/df_cidades_campi.csv"
    )

    df_mapas = pd.read_csv(
        "https://raw.githubusercontent.com/painelcovid19/painelcovid19.github.io/main/data/df_dados_acumulados.csv"
    )

    df_atualizacao = pd.read_csv(
        "https://raw.githubusercontent.com/painelcovid19/painelcovid19.github.io/main/data/last_update_dates.csv"
    )

df_cidades_campi["MovingMeanConfirmed"] = df_cidades_campi["new_confirmed"].rolling(14).mean()
df_cidades_campi["MovingMeanDeaths"] = df_cidades_campi["new_deaths"].rolling(14).mean()

df_redencao = df_cidades_campi.loc[(df_cidades_campi["city_ibge_code"] == 2311603)]
df_sfc = df_cidades_campi.loc[(df_cidades_campi["city_ibge_code"] == 2929206)]
df_acarape = df_cidades_campi.loc[(df_cidades_campi["city_ibge_code"] == 2300150)]

df_acarape_atualizacao = df_atualizacao.loc[(df_atualizacao["city"] == "Acarape")]
df_redencao_atualizacao = df_atualizacao.loc[(df_atualizacao["city"] == "Redenção")]
df_sfc_atualizacao = df_atualizacao.loc[(df_atualizacao["city"] == "São Francisco do Conde" )]




POPULACAO_ESTIMADA_ACARAPE = 15036  # https://www.ibge.gov.br/cidades-e-estados/ce/acarape.html
POPULACAO_ESTIMADA_REDENCAO = 29146  # https://www.ibge.gov.br/cidades-e-estados/ce/redencao.html
POPULACAO_ESTIMADA_SFC = (
    40245  # https://www.ibge.gov.br/cidades-e-estados/ba/sao-francisco-do-conde.html
)


def create_scatter_plot(df, _type, title):
    column = None

    if _type == "casos":
        column = "new_confirmed"
        moving_mean_column = "MovingMeanConfirmed"
    elif _type == "óbitos":
        column = "new_deaths"
        moving_mean_column = "MovingMeanDeaths"

    fig = go.Figure(
        layout=go.Layout(
            title=title,
            yaxis={"title": ""},
            xaxis={"title": ""},
            template="plotly_white",
            legend=dict(
                yanchor="top", y=0.99, xanchor="right", x=1, bordercolor="lightgrey", borderwidth=1
            ),
            height=400,
            width=650,
        )
    )
    fig.add_trace(
        go.Bar(
            x=df["date"],
            y=df[column],
            name=_type,
            marker_color="darkblue",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df[moving_mean_column],
            mode="lines",
            name="média móvel",
            marker_color="orange",
        )
    )
    fig.update_yaxes({"rangemode": "nonnegative"})

    return fig


# Casos Confirmados de Acarape e a Média Movel
confirmated_cases_acarape = create_scatter_plot(df_acarape, "casos", "Casos Confirmados em Acarape")

# Obitos de Acarape e a Média Movel
death_cases_acarape = create_scatter_plot(df_acarape, "óbitos", "Óbitos em Acarape")

# Casos Confirmados de Redenção e a Média Movel
confirmated_cases_redencao = create_scatter_plot(df_redencao, "casos", "Casos Confirmados em Redenção")

# Obitos de Redenção e Média Movel
death_cases_redencao = create_scatter_plot(df_redencao, "óbitos", "Óbitos em Redenção")

# Casos Confirmados de São Francisco de Conde e a Média Movel
confirmated_cases_SFC = create_scatter_plot(df_sfc, "casos", "Casos Confirmados em SFC")

# Obitos de São Francsico de Conde e Média Movel
death_cases_SFC = create_scatter_plot(df_sfc, "óbitos", "Óbitos em SFC")

# Mapas
ceara = df_mapas[df_mapas["state"] == "CE"]
municipios_CE = gpd.read_file("shapefiles/CE_Municipios_2020.shp")
campi_CE = municipios_CE.merge(
    ceara, left_on="NM_MUN", right_on="city", suffixes=("", "_y")
).set_index("city")

mapa_confirmados_ce = px.choropleth_mapbox(
    campi_CE,
    geojson=campi_CE.geometry,
    locations=campi_CE.index,
    color="last_available_confirmed_per_100k_inhabitants",
    labels={"last_available_confirmed_per_100k_inhabitants": ""},
    center={"lat": -4.4118, "lon": -38.7491},
    opacity=0.7,
    mapbox_style="carto-positron",
    title="Casos confirmados no Maciço de Baturité (por 100 mil hab.)",
    color_continuous_scale=px.colors.sequential.PuBuGn,
    zoom=7.75,
    height=400,
    width=650,
)

mapa_obitos_ce = px.choropleth_mapbox(
    campi_CE,
    geojson=campi_CE.geometry,
    locations=campi_CE.index,
    color="last_available_deaths_per_100k_inhabitants",
    labels={"last_available_deaths_per_100k_inhabitants": ""},
    center={"lat": -4.4118, "lon": -38.7491},
    opacity=0.7,
    mapbox_style="carto-positron",
    title="Óbitos no Maciço de Baturité (por 100 mil hab.)",
    color_continuous_scale=px.colors.sequential.Reds,
    zoom=7.75,
    height=400,
    width=650,
)

bahia = df_mapas[df_mapas["state"] == "BA"]
municipios_BA = gpd.read_file("shapefiles/BA_Municipios_2020.shp")
campi_BA = municipios_BA.merge(
    bahia, left_on="NM_MUN", right_on="city", suffixes=("", "_y")
).set_index("city")

mapa_confirmados_ba = px.choropleth_mapbox(
    campi_BA,
    geojson=campi_BA.geometry,
    locations=campi_BA.index,
    color="last_available_confirmed_per_100k_inhabitants",
    labels={"last_available_confirmed_per_100k_inhabitants": ""},
    center={"lat": -12.7089, "lon": -38.3354},
    opacity=0.7,
    mapbox_style="carto-positron",
    title="Casos confirmados na Região Metropolitana <br>de Salvador (por 100 mil hab.)",
    color_continuous_scale=px.colors.sequential.PuBuGn,
    zoom=7.75,
    height=400,
    width=650
)

mapa_obitos_ba = px.choropleth_mapbox(
    campi_BA,
    geojson=campi_BA.geometry,
    locations=campi_BA.index,
    color="last_available_deaths_per_100k_inhabitants",
    labels={"last_available_deaths_per_100k_inhabitants": ""},
    center={"lat": -12.7089, "lon": -38.3354},
    opacity=0.7,
    mapbox_style="carto-positron",
    # mapbox_style="stamen-toner",
    title="Óbitos na Região Metropolitana <br>de Salvador (por 100 mil hab.)",
    color_continuous_scale=px.colors.sequential.Reds,
    zoom=7.75,
    height=400,
    width=650
)




