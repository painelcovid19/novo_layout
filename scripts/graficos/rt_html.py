from datetime import datetime, timedelta, timezone
from packages.calculate_rt import  Calculate_Rt
import pandas as pd
from plotly.subplots import make_subplots


# if __debug__:
#     dados_campis = pd.read_csv("./data/dados_campis.csv", parse_dates=["date"])
# else:
#     dados_campis = pd.read_csv(
#         "https://raw.githubusercontent.com/painelcovid19/painelcovid19.github.io/main/data/df_dados_macro_regioes_ceara.csv"
#     )

dados_campis = pd.read_csv("./data/df_cidades_rt.csv", parse_dates=["date"])


df_redencao = dados_campis[dados_campis["city"] == "Redenção"]
df_acarape = dados_campis[dados_campis["city"] == "Acarape"]
df_SFC = dados_campis[dados_campis["city"] == "São Francisco do Conde"]
df_Fortaleza = dados_campis[dados_campis["city"] == "Fortaleza"]
df_Salvador = dados_campis[dados_campis["city"] == "Salvador"]


# criando os graficos 
rt = Calculate_Rt()

df_reformated_acarape = rt.ajust_numbers(df_acarape)
df_reformated_redencao = rt.ajust_numbers(df_redencao)
df_reformated_SFC = rt.ajust_numbers(df_SFC)
df_reformated_Fortaleza = rt.ajust_numbers(df_Fortaleza)
df_reformated_Salvador = rt.ajust_numbers(df_Salvador)


figure_acarape = rt.estimate_plotly(df_reformated_acarape, city_name="Acarape")
figure_SFC = rt.estimate_plotly(df_reformated_SFC, city_name="São Francisco do Conde")
figure_redencao = rt.estimate_plotly(df_reformated_redencao, city_name="Redenção")
figure_Fortaleza = rt.estimate_plotly(df_reformated_Fortaleza, city_name="Fortaleza")
figure_Salvador = rt.estimate_plotly(df_reformated_Salvador, city_name="Salvador")

graf = [figure_acarape,figure_SFC,figure_redencao,figure_Fortaleza,figure_Salvador]