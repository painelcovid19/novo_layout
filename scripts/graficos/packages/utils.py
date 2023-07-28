import logging
import numpy
import pandas as pd

s3_directory = "s3://painelcovid2023/data"

logging.basicConfig(level=logging.DEBUG)

def get_last_update_date(data):
    last_updates = {}
    for index, row in enumerate(data["new_confirmed"]):
        if row >= 1:
            last_updates["city"] = data["city"].iloc[index]
            last_updates["date"] = data.iloc[index, 2]
            break
    return last_updates

def get_datas(ibge_codes_list, df_of_cases):
    datas = []
    for cod in ibge_codes_list:
        df_row = df_of_cases[df_of_cases["ibgeID"] == cod]
        datas.append(df_row)
    return datas

def rename_city(city):
    city_name, uf = city.split("/")
    city = city_name
    return city

columns = ["city", "ibgeID", "date","state", "totalCases","deaths_per_100k_inhabitants", "totalCases_per_100k_inhabitants", "deaths", "newCases", "newDeaths"]
new_columns =["city", "city_ibge_code", "date", "state", "last_available_confirmed","last_available_deaths_per_100k_inhabitants", "last_available_confirmed_per_100k_inhabitants", "last_available_deaths", "new_confirmed", "new_deaths"]

def remove_negatives(list_entry):

  acc = 0  # accumulator
  for i, x in enumerate(list_entry): # percorre todos os elementos do array
    if x < 0:        # se for um valor negativo
      acc = acc + x  # decrementa o acumulador, pois x é negativo
      list_entry[i] = 0  # atribui zero na posição onde está negativo
      continue       # passa para o próximo elemento da lista
    
                            # se for um valor positivo, chegará nesse ponto (pula o if anterior)
    if acc < 0:              # se o acumulador for negativo   
      if x + acc < 0:        # e se x menos o acumulador for menor que zero
        list_entry[i] = 0        # zera a posição
        acc = acc + x        # atualiza o acumulador para "retirar" x unidades (x é positivo)
      else:                  # caso x menos o acumulador seja maior ou igual a zero
        list_entry[i] = x + acc  # o valor nessa posição é decrementado do valor do acumulador
        acc = 0              # zera o acumulador
  return list_entry


#           Datas da ultima actualização
dates = pd.read_csv(f"{s3_directory}/last_update_dates.csv")

last_actualization_date_acarape = dates[dates["city"] == "Acarape"]["dates"].loc[0]
last_actualization_date_redencao = dates[dates["city"] == "Redenção"]["dates"].loc[1]
last_actualization_date_SFC = dates[dates["city"] == "São Francisco do Conde"]["dates"].loc[2]


#           Dados acumulados
acumulated_data = pd.read_csv(f"{s3_directory}/df_dados_acumulados.csv")

acarape_total_confirmated_data = acumulated_data[acumulated_data["city"] == "Acarape"]["last_available_confirmed"].loc[0]
acarape_total_death_data = acumulated_data[acumulated_data["city"] == "Acarape"]["last_available_deaths"].loc[0]

redencao_total_confirmated_data = acumulated_data[acumulated_data["city"] == "Redenção"]["last_available_confirmed"].loc[18]
redencao_total_death_data = acumulated_data[acumulated_data["city"] == "Redenção"]["last_available_deaths"].loc[18]

SFC_total_confirmated_data = acumulated_data[acumulated_data["city"] == "São Francisco do Conde"]["last_available_confirmed"].loc[21]
SFC_tota_death_data = acumulated_data[acumulated_data["city"] == "São Francisco do Conde"]["last_available_deaths"].loc[21]




