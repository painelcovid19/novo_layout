from jinja2 import Environment, FileSystemLoader, select_autoescape
from plotly import express as px
from plotly.offline import plot
from plotly.graph_objs import Scatter
from scripts.graficos.main import (
    confirmated_cases_acarape,
    confirmated_cases_redencao,
    confirmated_cases_SFC,
    death_cases_acarape,
    death_cases_redencao,
    death_cases_SFC
)
from scripts.graficos.packages.utils import (
    last_actualization_date_acarape,
    last_actualization_date_redencao,
    last_actualization_date_SFC,

  acarape_total_confirmated_data,
  acarape_total_death_data,
  redencao_total_confirmated_data,
  redencao_total_death_data,
  SFC_total_confirmated_data,
  SFC_tota_death_data
)

loader = FileSystemLoader("template-teste-final/")
env = Environment(loader=loader, autoescape=select_autoescape())

templateinicio_b = env.get_template("inicio_b.html")
templateestimativas_b = env.get_template("estimativas_b.html")
templatemapas_b = env.get_template("mapas_b.html")
templatesobre_b = env.get_template("sobre_b.html")
templatevacina_b = env.get_template("vacina_b.html")

with open("index.html", "wb")  as index_file:

    output = templateinicio_b.render(title= "Painel Covid 19", 
        confirmated_acarape = confirmated_cases_acarape.to_html(full_html=False, include_plotlyjs=True),
        death_acarape = death_cases_acarape.to_html(full_html=False, include_plotlyjs=True),
        confirmated_redencao = confirmated_cases_redencao.to_html(full_html=False, include_plotlyjs=True),
        death_redencao = death_cases_redencao.to_html(full_html=False, include_plotlyjs=True),
        confirmated_SFC = confirmated_cases_SFC.to_html(full_html=False, include_plotlyjs=True),
        death_SFC = death_cases_SFC.to_html(full_html=False, include_plotlyjs=True),

        
        total_case_redencao = redencao_total_confirmated_data,
        total_death_redencao = redencao_total_death_data,
        last_actualization_redencao = last_actualization_date_redencao,

        total_case_acarape = acarape_total_confirmated_data,
        total_death_acarape = acarape_total_death_data,
        last_actualization_acarape = last_actualization_date_acarape,

        total_case_SFC = SFC_total_confirmated_data,
        total_death_SFC = SFC_tota_death_data,
        last_actualization_SFC = last_actualization_date_SFC

        )

    index_file.write(output.encode('utf-8'))


with open("vacina_s.html", "wb")  as index_file:

    output = templatevacina_b.render(title= "Painel Covid 19", Plot =confirmated_cases_acarape.to_html(full_html=False, include_plotlyjs=True))

    index_file.write(output.encode('utf-8'))


with open("mapas_s.html", "wb")  as index_file:

    output = templatemapas_b.render(title= "Painel Covid 19", Plot =confirmated_cases_redencao.to_html(full_html=False, include_plotlyjs=True), Plot1 =death_cases_acarape.to_html(full_html=False, include_plotlyjs=True), Plot2 =confirmated_cases_SFC.to_html(full_html=False, include_plotlyjs=True))

    index_file.write(output.encode('utf-8'))


with open("estimativas_s.html", "wb")  as index_file:

    output = templateestimativas_b.render(title = "Painel Covid 19", Plot =death_cases_redencao.to_html(full_html=False, include_plotlyjs=True), Plot1 =death_cases_SFC.to_html(full_html=False, include_plotlyjs=True), Plot2 =death_cases_SFC.to_html(full_html=False, include_plotlyjs=True))

    index_file.write(output.encode('utf-8'))


with open("sobre_s.html", "wb")  as index_file:

    output = templatesobre_b.render(title= "Painel Covid 19")

    index_file.write(output.encode('utf-8'))