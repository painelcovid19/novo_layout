from datetime import datetime, timedelta, timezone
from sys import stdout

# import geopandas as gpd
import pandas as pd
import plotly.graph_objects as go
from plotly import express as px
from plotly.subplots import make_subplots

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


# GRÁFICOS DE VACINADOS
if __debug__:
    vacina_redencao = pd.read_csv("./data/vaccines-redencao-ce.csv")
    vacina_acarape = pd.read_csv("./data/vaccines-acarape-ce.csv")
    vacina_SFC = pd.read_csv("./data/vaccines-sao-francisco-do-conde-ba.csv")

else:
    vacina_redencao = pd.read_csv(
        "https://raw.githubusercontent.com/painelcovid19/painelcovid19.github.io/main/data/vaccines-redencao-ce.csv"
    )
    vacina_acarape = pd.read_csv(
        "https://raw.githubusercontent.com/painelcovid19/painelcovid19.github.io/main/data/vaccines-acarape-ce.csv"
    )
    vacina_SFC = pd.read_csv(
        "https://raw.githubusercontent.com/painelcovid19/painelcovid19.github.io/main/data/vaccines-sao-francisco-do-conde-ba.csv"
    )

vacina_redencao["vacina_descricao_dose"] = vacina_redencao["vacina_descricao_dose"].str.replace(
    "\xa0", ""
)
vacina_acarape["vacina_descricao_dose"] = vacina_acarape["vacina_descricao_dose"].str.replace(
    "\xa0", ""
)
vacina_SFC["vacina_descricao_dose"] = vacina_SFC["vacina_descricao_dose"].str.replace("\xa0", "")

dose_1_acarape = vacina_acarape[vacina_acarape["vacina_descricao_dose"] == "1ª Dose"]
dose_2_acarape = vacina_acarape[vacina_acarape["vacina_descricao_dose"] == "2ª Dose"]
dose_acarape_unica = vacina_acarape[vacina_acarape["vacina_descricao_dose"] == "Dose"]
reforco_acarape = vacina_acarape[vacina_acarape["vacina_descricao_dose"] == "Reforço"]

dose_1_redencao = vacina_redencao[vacina_redencao["vacina_descricao_dose"] == "1ª Dose"]
dose_2_redencao = vacina_redencao[vacina_redencao["vacina_descricao_dose"] == "2ª Dose"]
dose_redencao_unica = vacina_redencao[vacina_redencao["vacina_descricao_dose"] == "Dose"]
reforco_redencao = vacina_redencao[vacina_redencao["vacina_descricao_dose"] == "Reforço"]

dose_1_sfc = vacina_SFC[vacina_SFC["vacina_descricao_dose"] == "1ª Dose"]
dose_2_sfc = vacina_SFC[vacina_SFC["vacina_descricao_dose"] == "2ª Dose"]
dose_sfc = vacina_SFC[vacina_SFC["vacina_descricao_dose"] == "Dose"]
reforco_sfc = vacina_SFC[vacina_SFC["vacina_descricao_dose"] == "Reforço"]


# In[204]:


POPULACAO_ESTIMADA_ACARAPE = 15036  # https://www.ibge.gov.br/cidades-e-estados/ce/acarape.html
POPULACAO_ESTIMADA_REDENCAO = 29146  # https://www.ibge.gov.br/cidades-e-estados/ce/redencao.html
POPULACAO_ESTIMADA_SFC = (
    40245  # https://www.ibge.gov.br/cidades-e-estados/ba/sao-francisco-do-conde.html
)


# In[205]:


# primeira dose acarape
falta_acarape_1 = POPULACAO_ESTIMADA_ACARAPE - len(dose_1_acarape.index)
labels_acarape_1 = ["Não vacinados", "1ª Dose"]
values_acarape_1 = [falta_acarape_1, len(dose_1_acarape.index)]
# segunda dose acarape
falta_acarape_2 = POPULACAO_ESTIMADA_ACARAPE - len(dose_2_acarape.index)
labels_acarape_2 = ["Não vacinados", "2ª Dose", "Única dose"]
values_acarape_2 = [falta_acarape_1, len(dose_2_acarape.index), len(dose_acarape_unica.index)]
# reforço dose acarape
falta_acarape_3 = POPULACAO_ESTIMADA_ACARAPE - len(reforco_acarape.index)
labels_acarape_3 = ["Não vacinados", "Dose de Reforço"]
values_acarape_3 = [falta_acarape_1, len(reforco_redencao.index)]

# primeira dose redençao
falta_redencao_1 = POPULACAO_ESTIMADA_REDENCAO - len(dose_1_redencao.index)
labels_redencao_1 = ["Não vacinados", "1ª Dose"]
values_redencao_1 = [falta_redencao_1, len(dose_1_redencao.index)]
# segunda dose redencao
falta_redencao_2 = POPULACAO_ESTIMADA_REDENCAO - len(dose_2_redencao.index)
labels_redencao_2 = ["Não vacinados", "2ª Dose", "Única dose"]
values_redencao_2 = [falta_redencao_1, len(dose_2_redencao.index), len(dose_redencao_unica.index)]
# reforço dose redenção
falta_redencao_3 = POPULACAO_ESTIMADA_REDENCAO - len(reforco_redencao.index)
labels_redencao_3 = ["Não vacinados", "Dose de Reforço"]
values_redencao_3 = [falta_redencao_1, len(reforco_redencao.index)]

# primeira dose SFC
falta_SFC_1 = POPULACAO_ESTIMADA_SFC - len(dose_1_sfc.index)
labels_SFC_1 = ["Não vacinados", "1ª Dose"]
values_SFC_1 = [falta_SFC_1, len(dose_1_sfc.index)]
# segunda dose SFC
falta_SFC_2 = POPULACAO_ESTIMADA_SFC - len(dose_2_sfc.index)
labels_SFC_2 = ["Não vacinados", "2ª Dose", "Única dose"]
values_SFC_2 = [falta_SFC_2, len(dose_2_sfc.index), len(dose_sfc.index)]
# reforço dose SFC
falta_SFC_3 = POPULACAO_ESTIMADA_SFC - len(reforco_sfc.index)
labels_SFC_3 = ["Não vacinados", "Dose de Reforço"]
values_SFC_3 = [falta_SFC_2,  len(reforco_sfc.index)]

c = ["#dee1e3", "#0793f0"]


# In[206]:


values_SFC_2


# In[207]:


from plotly import express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

acarape_vac = make_subplots(rows=1, cols=3, specs=[[{"type": "domain"}, {"type": "domain"}, {"type": "domain"}]])
acarape_vac.add_trace(
    go.Pie(
        labels=labels_acarape_1,
        values=values_acarape_1,
        marker_colors=["#f2f7f7", "#7FFFD4"],
        name=" ",
    ),
    1,
    1,
)
acarape_vac.add_trace(
    go.Pie(
        labels=labels_acarape_2,
        values=values_acarape_2,
        marker_colors=["#f2f7f7", "#00FA9A", "#40E0D0"],
        name=" ",
    ),
    1,
    2,
)
acarape_vac.add_trace(
    go.Pie(
        labels=labels_acarape_3,
        values=values_acarape_3,
        marker_colors=["#f2f7f7", "#00FA9A", "#40E0D0"],
        name=" ",
    ),
    1,
    3,
)

# Use `hole` to create a donut-like pie chart
acarape_vac.update_traces(hole=0.7, hoverinfo="label+percent+name")

acarape_vac.update_layout(
    showlegend=False,
    height=350,
    width=500,
    title_text="Vacinados em Acarape",
    # Add annotations in the center of the donut pies.
    annotations=[
        dict(text="1ª dose", x=0.125, y=0.5, font_size=20, showarrow=False),
        dict(text="2ª dose e única", x=0.935, y=0.5, font_size=20, showarrow=False),
        dict(text="Dose de reforço", x=0.935, y=0.5, font_size=20, showarrow=False),
    ],
)


# In[208]:


# Create subplots: use 'domain' type for Pie subplot
redencao_vac = make_subplots(rows=1, cols=3, specs=[[{"type": "domain"}, {"type": "domain"}, {"type": "domain"}]])
redencao_vac.add_trace(
    go.Pie(
        labels=labels_redencao_1,
        values=values_redencao_1,
        marker_colors=["#f2f7f7", "#7FFFD4"],
        name=" ",
    ),
    1,
    1,
)
redencao_vac.add_trace(
    go.Pie(
        labels=labels_redencao_2,
        values=values_redencao_2,
        marker_colors=["#f2f7f7", "#00FA9A", "#40E0D0"],
        name=" ",
    ),
    1,
    2,
)
redencao_vac.add_trace(
    go.Pie(
        labels=labels_redencao_3,
        values=values_redencao_3,
        marker_colors=["#f2f7f7", "#00FA9A", "#40E0D0"],
        name=" ",
    ),
    1,
    3,
)

# Use `hole` to create a donut-like pie chart
redencao_vac.update_traces(hole=0.7, hoverinfo="label+percent+name")

redencao_vac.update_layout(
    showlegend=False,
    height=350,
    width=500,
    title_text="Vacinados em Redenção",
    # Add annotations in the center of the donut pies.
    annotations=[
        dict(text="1ª dose", x=0.125, y=0.5, font_size=20, showarrow=False),
        dict(text="2ª dose e única", x=0.935, y=0.5, font_size=20, showarrow=False),
        dict(text="Dose de reforço", x=0.935, y=0.5, font_size=20, showarrow=False),
    ],
)


# In[209]:


# Create subplots: use 'domain' type for Pie subplot
sfc_vac = make_subplots(rows=1, cols=3, specs=[[{"type": "domain"}, {"type": "domain"}, {"type": "domain"}]])
sfc_vac.add_trace(
    go.Pie(
        labels=labels_SFC_1, values=values_SFC_1, marker_colors=["#f2f7f7", "#7FFFD4"], name=" "
    ),
    1,
    1,
)
sfc_vac.add_trace(
    go.Pie(
        labels=labels_SFC_2,
        values=values_SFC_2,
        marker_colors=["#f2f7f7", "#00FA9A", "#40E0D0"],
        name=" ",
    ),
    1,
    2,
)
sfc_vac.add_trace(
    go.Pie(
        labels=labels_SFC_3,
        values=values_SFC_3,
        marker_colors=["#f2f7f7", "#00FA9A", "#40E0D0"],
        name=" ",
    ),
    1,
    3,
)

# Use `hole` to create a donut-like pie chart
sfc_vac.update_traces(hole=0.7, hoverinfo="label+percent+name")

sfc_vac.update_layout(
    showlegend=False,
    height=350,
    width=500,
    title_text="Vacinados em SFC",
    # Add annotations in the center of the donut pies.
    annotations=[
        dict(text="1ª dose", x=0.125, y=0.5, font_size=20, showarrow=False),
        dict(text="2ª dose e única", x=0.935, y=0.5, font_size=20, showarrow=False),
        dict(text="Dose de reforço", x=0.935, y=0.5, font_size=20, showarrow=False),
    ],
)


# In[210]:


# TESTE
vacinas = make_subplots(
    rows=3,
    cols=3,
    specs=[
        [{"type": "domain"}, {"type": "domain"}, {"type": "domain"}],
        [{"type": "domain"}, {"type": "domain"}, {"type": "domain"}],
        [{"type": "domain"}, {"type": "domain"}, {"type": "domain"}]
    ],
)

# ACARAPE
vacinas.add_trace(
    go.Pie(
        labels=labels_acarape_1,
        values=values_acarape_1,
        marker_colors=["#f2f7f7", "#7FFFD4"],
        name=" ",
    ),
    1,
    1,
)

vacinas.add_trace(
    go.Pie(
        labels=labels_acarape_2,
        values=values_acarape_2,
        marker_colors=["#f2f7f7", "#00FA9A", "#40E0D0"],
        name=" ",
    ),
    2,
    1,
)
vacinas.add_trace(
    go.Pie(
        labels=labels_acarape_3,
        values=values_acarape_3,
        marker_colors=["#f2f7f7", "#446fd4", "#40E0D0"],
        name=" ",
    ),
    3,
    1,
)
# REDENÇÃO
vacinas.add_trace(
    go.Pie(
        labels=labels_redencao_1,
        values=values_redencao_1,
        marker_colors=["#f2f7f7", "#7FFFD4"],
        name=" ",
    ),
    1,
    2,
)

vacinas.add_trace(
    go.Pie(
        labels=labels_redencao_2,
        values=values_redencao_2,
        marker_colors=["#f2f7f7", "#00FA9A", "#40E0D0"],
        name=" ",
    ),
    2,
    2,
)
vacinas.add_trace(
    go.Pie(
        labels=labels_redencao_3,
        values=values_redencao_3,
        marker_colors=["#f2f7f7", "#446fd4", "#40E0D0"],
        name=" ",
    ),
    3,
    2,
)

# SFC
vacinas.add_trace(
    go.Pie(
        labels=labels_SFC_1, values=values_SFC_1, marker_colors=["#f2f7f7", "#7FFFD4"], name=" "
    ),
    1,
    3,
)

vacinas.add_trace(
    go.Pie(
        labels=labels_SFC_2,
        values=values_SFC_2,
        marker_colors=["#f2f7f7", "#00FA9A", "#40E0D0"],
        name=" ",
    ),
    2,
    3,
)
vacinas.add_trace(
    go.Pie(
        labels=labels_SFC_3,
        values=values_SFC_3,
        marker_colors=["#f2f7f7", "#446fd4", "#40E0D0"],
        name=" ",
    ),
    3,
    3,
)


# In[211]:



# Use `hole` to create a donut-like pie chart
vacinas.update_traces(hole=0.7, hoverinfo="label+percent+name")
vacinas.update_layout(
    height=800,
    width=1000,
    legend=dict(orientation="h", yanchor="bottom", y=-0.09, xanchor="right", x=0.75),
    title_text=" ",
    # Add annotations in the center of the donut pies.
    annotations=[
        dict(text="1ª dose", x=0.11, y=0.88, font_size=12, showarrow=False),
        dict(text="1ª dose", x=0.5, y=0.88, font_size=12, showarrow=False),
        dict(text="1ª dose", x=0.89, y=0.88, font_size=12, showarrow=False),
        dict(text="2ª dose e única", x=0.086, y=0.5, font_size=12, showarrow=False),
        dict(text="2ª dose e única", x=0.5, y=0.5, font_size=12, showarrow=False),
        dict(text="2ª dose e única", x=0.915, y=0.5, font_size=12, showarrow=False),
        dict(text="Dose de Reforço", x=0.085, y=0.12, font_size=12, showarrow=False),
        dict(text="Dose de Reforço", x=0.5, y=0.12, font_size=12, showarrow=False),
        dict(text="Dose de Reforço", x=0.915, y=0.12, font_size=12, showarrow=False),
        dict(text="Acarape", x=0.09, y=1.1, font_size=18, showarrow=False),
        dict(text="Redenção", x=0.489, y=1.1, font_size=18, showarrow=False),
        dict(text="SFC", x=0.87, y=1.1, font_size=18, showarrow=False),
    ],
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
# ceara = df_mapas[df_mapas["state"] == "CE"]
# municipios_CE = gpd.read_file("shapefiles/CE_Municipios_2020.shp")
# campi_CE = municipios_CE.merge(
#     ceara, left_on="NM_MUN", right_on="city", suffixes=("", "_y")
# ).set_index("city")

# mapa_confirmados_ce = px.choropleth_mapbox(
#     campi_CE,
#     geojson=campi_CE.geometry,
#     locations=campi_CE.index,
#     color="last_available_confirmed_per_100k_inhabitants",
#     labels={"last_available_confirmed_per_100k_inhabitants": ""},
#     center={"lat": -4.4118, "lon": -38.7491},
#     opacity=0.7,
#     mapbox_style="carto-positron",
#     title="Casos confirmados no Maciço de Baturité (por 100 mil hab.)",
#     color_continuous_scale=px.colors.sequential.PuBuGn,
#     zoom=7.75,
#     height=400,
#     width=650,
# )

# mapa_obitos_ce = px.choropleth_mapbox(
#     campi_CE,
#     geojson=campi_CE.geometry,
#     locations=campi_CE.index,
#     color="last_available_deaths_per_100k_inhabitants",
#     labels={"last_available_deaths_per_100k_inhabitants": ""},
#     center={"lat": -4.4118, "lon": -38.7491},
#     opacity=0.7,
#     mapbox_style="carto-positron",
#     title="Óbitos no Maciço de Baturité (por 100 mil hab.)",
#     color_continuous_scale=px.colors.sequential.Reds,
#     zoom=7.75,
#     height=400,
#     width=650,
# )

# bahia = df_mapas[df_mapas["state"] == "BA"]
# municipios_BA = gpd.read_file("shapefiles/BA_Municipios_2020.shp")
# campi_BA = municipios_BA.merge(
#     bahia, left_on="NM_MUN", right_on="city", suffixes=("", "_y")
# ).set_index("city")

# mapa_confirmados_ba = px.choropleth_mapbox(
#     campi_BA,
#     geojson=campi_BA.geometry,
#     locations=campi_BA.index,
#     color="last_available_confirmed_per_100k_inhabitants",
#     labels={"last_available_confirmed_per_100k_inhabitants": ""},
#     center={"lat": -12.7089, "lon": -38.3354},
#     opacity=0.7,
#     mapbox_style="carto-positron",
#     title="Casos confirmados na Região Metropolitana <br>de Salvador (por 100 mil hab.)",
#     color_continuous_scale=px.colors.sequential.PuBuGn,
#     zoom=7.75,
#     height=400,
#     width=650
# )

# mapa_obitos_ba = px.choropleth_mapbox(
#     campi_BA,
#     geojson=campi_BA.geometry,
#     locations=campi_BA.index,
#     color="last_available_deaths_per_100k_inhabitants",
#     labels={"last_available_deaths_per_100k_inhabitants": ""},
#     center={"lat": -12.7089, "lon": -38.3354},
#     opacity=0.7,
#     mapbox_style="carto-positron",
#     # mapbox_style="stamen-toner",
#     title="Óbitos na Região Metropolitana <br>de Salvador (por 100 mil hab.)",
#     color_continuous_scale=px.colors.sequential.Reds,
#     zoom=7.75,
#     height=400,
#     width=650
# )



