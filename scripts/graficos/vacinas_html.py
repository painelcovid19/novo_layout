from datetime import datetime, timedelta, timezone
import pandas as pd
import plotly.graph_objs as go
import numpy as np
from plotly.subplots import make_subplots


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

POPULACAO_ESTIMADA_ACARAPE = 15036  # https://www.ibge.gov.br/cidades-e-estados/ce/acarape.html
POPULACAO_ESTIMADA_REDENCAO = 29146  # https://www.ibge.gov.br/cidades-e-estados/ce/redencao.html
POPULACAO_ESTIMADA_SFC = (
    40245  # https://www.ibge.gov.br/cidades-e-estados/ba/sao-francisco-do-conde.html
)



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

# vacinas Acarape
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

# vacinas redenção 
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

# vacinas São Francisco do Conde 
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


# Vacinas por faixa etária 

vacina_redencao_d1 = vacina_redencao.loc[vacina_redencao['vacina_descricao_dose']=='1ª Dose']
vacina_redencao_d2 = vacina_redencao.loc[vacina_redencao['vacina_descricao_dose']=='2ª Dose']
vacina_redencao_reforco = vacina_redencao.loc[vacina_redencao['vacina_descricao_dose']=='Reforço']
vacina_acarape_d1 = vacina_acarape.loc[vacina_acarape['vacina_descricao_dose']=='1ª Dose']
vacina_acarape_d2 = vacina_acarape.loc[vacina_acarape['vacina_descricao_dose']=='2ª Dose']
vacina_acarape_reforco = vacina_acarape.loc[vacina_acarape['vacina_descricao_dose']=='Reforço']
vacina_SFC_d1 = vacina_SFC.loc[vacina_SFC['vacina_descricao_dose']=='1ª Dose']
vacina_SFC_d2 = vacina_SFC.loc[vacina_SFC['vacina_descricao_dose']=='2ª Dose']
vacina_SFC_reforco = vacina_SFC.loc[vacina_SFC['vacina_descricao_dose']=='Reforço']

vacina_redencao_d1_fem = vacina_redencao_d1.loc[vacina_redencao_d1['paciente_enumSexoBiologico']=='F']
vacina_redencao_d1_mas = vacina_redencao_d1.loc[vacina_redencao_d1['paciente_enumSexoBiologico']=='M']
vacina_redencao_d2_fem = vacina_redencao_d2.loc[vacina_redencao_d2['paciente_enumSexoBiologico']=='F']
vacina_redencao_d2_mas = vacina_redencao_d2.loc[vacina_redencao_d2['paciente_enumSexoBiologico']=='M']
vacina_redencao_reforco_fem = vacina_redencao_reforco.loc[vacina_redencao_reforco['paciente_enumSexoBiologico']=='F']
vacina_redencao_reforco_mas = vacina_redencao_reforco.loc[vacina_redencao_reforco['paciente_enumSexoBiologico']=='M']

vacina_acarape_d1_fem = vacina_acarape_d1.loc[vacina_acarape_d1['paciente_enumSexoBiologico']=='F']
vacina_acarape_d1_mas = vacina_acarape_d1.loc[vacina_acarape_d1['paciente_enumSexoBiologico']=='M']
vacina_acarape_d2_fem = vacina_acarape_d2.loc[vacina_acarape_d2['paciente_enumSexoBiologico']=='F']
vacina_acarape_d2_mas = vacina_acarape_d2.loc[vacina_acarape_d2['paciente_enumSexoBiologico']=='M']
vacina_acarape_reforco_fem = vacina_acarape_reforco.loc[vacina_acarape_reforco['paciente_enumSexoBiologico']=='F']
vacina_acarape_reforco_mas = vacina_acarape_reforco.loc[vacina_acarape_reforco['paciente_enumSexoBiologico']=='M']

vacina_SFC_d1_fem = vacina_SFC_d1.loc[vacina_SFC_d1['paciente_enumSexoBiologico']=='F']
vacina_SFC_d1_mas = vacina_SFC_d1.loc[vacina_SFC_d1['paciente_enumSexoBiologico']=='M']
vacina_SFC_d2_fem = vacina_SFC_d2.loc[vacina_SFC_d2['paciente_enumSexoBiologico']=='F']
vacina_SFC_d2_mas = vacina_SFC_d2.loc[vacina_SFC_d2['paciente_enumSexoBiologico']=='M']
vacina_SFC_reforco_fem = vacina_SFC_reforco.loc[vacina_SFC_reforco['paciente_enumSexoBiologico']=='F']
vacina_SFC_reforco_mas = vacina_SFC_reforco.loc[vacina_SFC_reforco['paciente_enumSexoBiologico']=='M']


# Grafico de Faixa Etária - Vacinas por Faixa etária

redencao_etaria_fem1 = vacina_redencao_d1_fem['paciente_idade'].value_counts(sort=False, ascending=False, bins=12)
redencao_etaria_mas1 = vacina_redencao_d1_mas['paciente_idade'].value_counts(sort=False, ascending=False, bins=12)
redencao_etaria_fem2 = vacina_redencao_d2_fem['paciente_idade'].value_counts(sort=False, ascending=False, bins=12)
redencao_etaria_mas2 = vacina_redencao_d2_mas['paciente_idade'].value_counts(sort=False, ascending=False, bins=12)
redencao_etaria_fem_reforco = vacina_redencao_reforco_fem['paciente_idade'].value_counts(sort=False, ascending=False, bins=12)
redencao_etaria_mas_reforco = vacina_redencao_reforco_mas['paciente_idade'].value_counts(sort=False, ascending=False, bins=12)

acarape_etaria_fem1 = vacina_acarape_d1_fem['paciente_idade'].value_counts(sort=False, ascending=False, bins=12)
acarape_etaria_mas1 = vacina_acarape_d1_mas['paciente_idade'].value_counts(sort=False, ascending=False, bins=12)
acarape_etaria_fem2 = vacina_acarape_d2_fem['paciente_idade'].value_counts(sort=False, ascending=False, bins=12)
acarape_etaria_mas2 = vacina_acarape_d2_mas['paciente_idade'].value_counts(sort=False, ascending=False, bins=12)
acarape_etaria_fem_reforco = vacina_acarape_reforco_fem['paciente_idade'].value_counts(sort=False, ascending=False, bins=12)
acarape_etaria_mas_reforco = vacina_acarape_reforco_mas['paciente_idade'].value_counts(sort=False, ascending=False, bins=12)

sfc_etaria_fem1 = vacina_SFC_d1_fem['paciente_idade'].value_counts(sort=False, ascending=False, bins=12)
sfc_etaria_mas1 = vacina_SFC_d1_mas['paciente_idade'].value_counts(sort=False, ascending=False, bins=12)
sfc_etaria_fem2 = vacina_SFC_d2_fem['paciente_idade'].value_counts(sort=False, ascending=False, bins=12)
sfc_etaria_mas2 = vacina_SFC_d2_mas['paciente_idade'].value_counts(sort=False, ascending=False, bins=12)
sfc_etaria_fem_reforco = vacina_SFC_reforco_fem['paciente_idade'].value_counts(sort=False, ascending=False, bins=12)
sfc_etaria_mas_reforco = vacina_SFC_reforco_mas['paciente_idade'].value_counts(sort=False, ascending=False, bins=12)

FaixaEtaria = ['0-10','10-20','20-30','30-40','40-50','50-60','60-70','70-80','80-90','90-100','100-110','110-120']

df_redencao_etaria_fem1=pd.DataFrame(FaixaEtaria, redencao_etaria_fem1).reset_index()
df_redencao_etaria_mas1=pd.DataFrame(FaixaEtaria, redencao_etaria_mas1).reset_index()
df_redencao_etaria_fem2=pd.DataFrame(FaixaEtaria, redencao_etaria_fem2).reset_index()
df_redencao_etaria_mas2=pd.DataFrame(FaixaEtaria, redencao_etaria_mas2).reset_index()
df_redencao_etaria_fem_reforco=pd.DataFrame(FaixaEtaria, redencao_etaria_fem_reforco).reset_index()
df_redencao_etaria_mas_reforco=pd.DataFrame(FaixaEtaria, redencao_etaria_mas_reforco).reset_index()


mulheres_dose1 = np.array(redencao_etaria_fem1)
mulheres_dose2 = np.array(redencao_etaria_fem2)
mulheres_reforco = np.array(redencao_etaria_fem_reforco)
homens_dose1 = np.array(redencao_etaria_mas1)*-1
homens_dose2 = np.array(redencao_etaria_mas2)*-1
homens_reforco = np.array(redencao_etaria_mas_reforco)*-1
#women_with_dogs_bins = np.array(redencao_etaria_fem_reforco)
#men_with_dogs_bins = np.array(redencao_etaria_fem_reforco)

#y = list(range(0, 130, 10))
y=FaixaEtaria

layout = go.Layout(yaxis=go.layout.YAxis(title='Faixa Etária'),
                   xaxis=go.layout.XAxis(
                       range=[-3000, 3000],
                       tickvals=[-3000, -2500, -2000, -1500, -1000, -500, 0, 500, 1000, 1500, 2000, 2500, 3500],
                       ticktext=[3000, 2500, 2000, 1500, 1000, 500, 0, 500, 1000, 1500, 2000, 2500, 3500],
                       title=' '),
                   barmode='overlay',
                   bargap=0.1)

data = [go.Bar(y=y,
               x=mulheres_dose1,
               orientation='h',
               name='1ª dose em mulheres',
               hoverinfo='x',
               marker=dict(color='#40E0D0')
               ),
        go.Bar(y=y,
               x=mulheres_dose2,
               orientation='h',
               name='2ª dose em mulheres',
               #text=-1 * women_bins.astype('int'),
               hoverinfo='x',
               marker=dict(color='#00FA9A')
               ),
        go.Bar(y=y,
               x=mulheres_reforco,
               orientation='h',
               name='Dose reforço em mulheres',
               #text=-1 * women_bins.astype('int'),
               hoverinfo='x',
               opacity=0.5,
               marker=dict(color='#076cf0')
               ),
        go.Bar(y=y,
               x=homens_dose1,
               orientation='h',
               name='1ª dose em homens',
               text=-1 * homens_dose1.astype('int'),
               hoverinfo='text',
               marker=dict(color='#40E0D0')
               ),
        go.Bar(y=y,
               x=homens_dose2,
               orientation='h',
               name='2ª dose em homens',
               text=-1 * homens_dose2.astype('int'),
               hoverinfo='text',
               marker=dict(color='#00FA9A')
               ),
        go.Bar(y=y,
               x=homens_reforco,
               orientation='h',
               name='Dose reforço em homens',
               text=-1 * homens_reforco.astype('int'),
               hoverinfo='text',
               opacity=0.5,
               marker=dict(color='#076cf0')
               ),
        #go.Bar(y=y,
         #      x=homens_dose1,
          #     orientation='h',
           #    hoverinfo='x',
            #   showlegend=False,
             #  opacity=0.5,
              # marker=dict(color='teal')
               #),
        #go.Bar(y=y,
        #       x=women_with_dogs_bins,
       #        orientation='h',
        #       text=-1 * women_bins.astype('int'),
        #       hoverinfo='text',
        #       showlegend=False,
        #       opacity=0.5,
         #      marker=dict(color='darkgreen')
               #)
               ]

# pio.show(dict(data=data, layout=layout), filename='EXAMPLES/stacked_bar_pyramid')

mulheres_dose1 = np.array(acarape_etaria_fem1)
mulheres_dose2 = np.array(acarape_etaria_fem2)
mulheres_reforco = np.array(acarape_etaria_fem_reforco)
homens_dose1 = np.array(acarape_etaria_mas1)*-1
homens_dose2 = np.array(acarape_etaria_mas2)*-1
homens_reforco = np.array(acarape_etaria_mas_reforco)*-1
#women_with_dogs_bins = np.array(redencao_etaria_fem_reforco)
#men_with_dogs_bins = np.array(redencao_etaria_fem_reforco)

#y = list(range(0, 130, 10))
y=FaixaEtaria

layout = go.Layout(yaxis=go.layout.YAxis(title='Faixa Etária'),
                   xaxis=go.layout.XAxis(
                       range=[-1000, 1000],
                       tickvals=[-1000, -500, 0, 500, 1000],
                       ticktext=[1000, 500, 0, 500, 1000],
                       title='Number'),
                   barmode='overlay',
                   bargap=0.1)

data = [go.Bar(y=y,   
               x=mulheres_dose1,
               orientation='h',
               name='1ª dose em mulheres',
               hoverinfo='x',
               marker=dict(color='#40E0D0')
               ),
        go.Bar(y=y,
               x=mulheres_dose2,
               orientation='h',
               name='2ª dose em mulheres',
               #text=-1 * women_bins.astype('int'),
               hoverinfo='text',
               marker=dict(color='#00FA9A')
               ),
        go.Bar(y=y,
               x=mulheres_reforco,
               orientation='h',
               name='Dose reforço em mulheres',
               #text=-1 * women_bins.astype('int'),
               hoverinfo='text',
               opacity=0.8,
               marker=dict(color='#076cf0')
               ),
        go.Bar(y=y,
               x=homens_dose1,
               orientation='h',
               name='1ª dose em homens',
               text=-1 * homens_dose1.astype('int'),
               hoverinfo='text',
               marker=dict(color='#40E0D0')
               ),
        go.Bar(y=y,
               x=homens_dose2,
               orientation='h',
               name='2ª dose em homens',
               text=-1 * homens_dose2.astype('int'),
               hoverinfo='text',
               marker=dict(color='#00FA9A')
               ),
        go.Bar(y=y,
               x=homens_reforco,
               orientation='h',
               name='Dose reforço em homens',
               text=-1 * homens_reforco.astype('int'),
               hoverinfo='text',
               opacity=0.8,
               marker=dict(color='#076cf0')
               ),
        #go.Bar(y=y,
         #      x=homens_dose1,
          #     orientation='h',
           #    hoverinfo='x',
            #   showlegend=False,
             #  opacity=0.5,
              # marker=dict(color='teal')
               #),
        #go.Bar(y=y,
        #       x=women_with_dogs_bins,
       #        orientation='h',
        #       text=-1 * women_bins.astype('int'),
        #       hoverinfo='text',
        #       showlegend=False,
        #       opacity=0.5,
         #      marker=dict(color='darkgreen')
               #)
               ]

# pio.show(dict(data=data, layout=layout), filename='EXAMPLES/stacked_bar_pyramid')

mulheres_dose1 = np.array(sfc_etaria_fem1)
mulheres_dose2 = np.array(sfc_etaria_fem2)
mulheres_reforco = np.array(sfc_etaria_fem_reforco)
homens_dose1 = np.array(sfc_etaria_mas1)*-1
homens_dose2 = np.array(sfc_etaria_mas2)*-1
homens_reforco = np.array(sfc_etaria_mas_reforco)*-1
#women_with_dogs_bins = np.array(redencao_etaria_fem_reforco)
#men_with_dogs_bins = np.array(redencao_etaria_fem_reforco)

#y = list(range(0, 130, 10))
y=FaixaEtaria

layout = go.Layout(yaxis=go.layout.YAxis(title='Faixa Etária'),
                   xaxis=go.layout.XAxis(
                       #range=[-4000, 4000],
                       tickvals=[-3500, -3000, -2500, -2000, -1500, -1000, -500, 0, 500, 1000, 1500, 2000, 2500, 3000, 3500],
                       ticktext=[3500, 3000, 2500, 2000, 1500, 1000, 500, 0, 500, 1000, 1500, 2000, 2500, 3000, 3500],
                       title=' '),
                   barmode='overlay',
                   bargap=0.2)

data = [go.Bar(y=y,
               x=mulheres_dose1,
               orientation='h',
               name='1ª dose em mulheres',
               hoverinfo='x',
               #opacity=0.5,
               marker=dict(color='#40E0D0')
               ),
        go.Bar(y=y,
               x=mulheres_dose2,
               orientation='h',
               name='2ª dose em mulheres',
               #text=-1 * women_bins.astype('int'),
               hoverinfo='text',
               #opacity=0.5,
               marker=dict(color='#00FA9A')
               ),
        go.Bar(y=y,
               x=mulheres_reforco,
               orientation='h',
               name='Dose reforço em mulheres',
               #text=-1 * women_bins.astype('int'),
               hoverinfo='text',
               opacity=0.8,
               marker=dict(color='#076cf0')
               ),
        go.Bar(y=y,
               x=homens_dose1,
               orientation='h',
               name='1ª dose em homens',
               #text=-1 * homens_dose1.astype('int'),
               hoverinfo='text',
               #opacity=0.5,
               marker=dict(color='#40E0D0')
               ),
        go.Bar(y=y,
               x=homens_dose2,
               orientation='h',
               name='2ª dose em homens',
               #text=-1 * homens_dose2.astype('int'),
               hoverinfo='text',
               #opacity=0.2,
               marker=dict(color='#00FA9A')
               ),
        go.Bar(y=y,
               x=homens_reforco,
               orientation='h',
               name='Dose reforço em homens',
               #text=-1 * homens_reforco.astype('int'),
               text = sfc_etaria_mas_reforco.astype('int'),
               hoverinfo='text',
               opacity=0.8,
               marker=dict(color='#076cf0')
               ),
        #go.Bar(y=y,
         #      x=homens_dose1,
          #     orientation='h',
           #    hoverinfo='x',
            #   showlegend=False,
             #  opacity=0.5,
              # marker=dict(color='teal')
               #),
        #go.Bar(y=y,
        #       x=women_with_dogs_bins,
       #        orientation='h',
        #       text=-1 * women_bins.astype('int'),
        #       hoverinfo='text',
        #       showlegend=False,
        #       opacity=0.5,
         #      marker=dict(color='darkgreen')
               #)
               ]

# pio.to_html(dict(data=data, layout=layout)

vacinas.write_html("vaci_teste.html")