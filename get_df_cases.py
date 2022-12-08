import pandas as pd
import numpy
import os
import csv
from packages.utils import get_last_update_date, rename_city, remove_negatives


columns = [
    "city",
     "ibgeID", 
     "date",
     "state", 
     "totalCases",
      "totalCases_per_100k_inhabitants", 
      "deaths", 
      "newCases", 
      "newDeaths"
      ]

campis_url = "https://github.com/wcota/covid19br/blob/master/cases-brazil-cities-time_changesOnly.csv.gz?raw=true"
rt_url = "https://github.com/wcota/covid19br/blob/master/cases-brazil-cities-time.csv.gz?raw=true"

def get_dataset(url):

    df_cases = pd.read_csv(url, compression='gzip')

    df_filter = (df_cases["city"] == "Acarape/CE") | (df_cases["city"] == "Redenção/CE") | (df_cases["city"] == "São Francisco do Conde/BA") \
    | (df_cases["city"] == "Fortaleza/CE") | (df_cases["city"] == "Salvador/BA") 

    df_cities = df_cases[df_filter][columns]

    df_cities.columns = ["city", "city_ibge_code", "date", "state", "last_available_confirmed", "last_available_confirmed_per_100k_inhabitants", "last_available_deaths", "new_confirmed", "new_deaths"]

    df_cities = df_cities.sort_values(by="city")
    df_cities["city"] = df_cities["city"].apply(rename_city)

    #Acarape
    df_Acarape = df_cities[df_cities["city"] == "Acarape"].sort_values(by="date", ascending=False)
    out_acarape_new_confirmed = remove_negatives( list(df_Acarape["new_confirmed"].values))
    out_acarape_new_deaths = remove_negatives(list(df_Acarape["new_deaths"].values))
    df_Acarape.loc[ : , "new_confirmed"] = out_acarape_new_confirmed
    df_Acarape["new_deaths"] = out_acarape_new_deaths

    
    #Redenção
    df_Redencao = df_cities[df_cities["city"] == "Redenção"].sort_values(by="date", ascending=False)
    out_redencao_new_confirmed = remove_negatives(list(df_Redencao["new_confirmed"].values))
    out_redencao_new_new_new_deaths = remove_negatives(list(df_Redencao["new_deaths"].values))
    df_Redencao["new_confirmed"] =out_redencao_new_confirmed
    df_Redencao["new_deaths"] = out_redencao_new_new_new_deaths

    #São Francisco do Conde
    df_SFC = df_cities[df_cities["city"] == "São Francisco do Conde"].sort_values(by="date", ascending=False)
    out_SFC_new_confirmed = remove_negatives(list(df_SFC["new_confirmed"].values))
    out_SFC_new_deaths = remove_negatives(list(df_SFC["new_deaths"].values))
    df_SFC["new_confirmed"] =out_SFC_new_confirmed
    df_SFC["new_deaths"] = out_SFC_new_deaths

    #Fortaleza
    df_Fortaleza = df_cities[df_cities["city"] == "Fortaleza"].sort_values(by="date", ascending=False)
    out_fortaleza_new_confirmed = remove_negatives(list(df_Fortaleza["new_confirmed"].values))
    out_fortaleza_new_new_new_deaths = remove_negatives(list(df_Fortaleza["new_deaths"].values))
    df_Fortaleza["new_confirmed"] =out_fortaleza_new_confirmed
    df_Fortaleza["new_deaths"] = out_fortaleza_new_new_new_deaths


    #Salvador
    df_Salvador = df_cities[df_cities["city"] == "Salvador"].sort_values(by="date", ascending=False)
    out_salvador_new_confirmed = remove_negatives(list(df_Salvador["new_confirmed"].values))
    out_salvador_new_new_new_deaths = remove_negatives(list(df_Salvador["new_deaths"].values))
    df_Salvador["new_confirmed"] =out_salvador_new_confirmed
    df_Salvador["new_deaths"] = out_salvador_new_new_new_deaths

    df_cities = pd.concat([df_Acarape, df_Redencao, df_SFC, df_Fortaleza, df_Salvador])
    df_cities.reset_index(inplace=True)
    df_cities.drop("index", axis=1, inplace=True)

    return df_cities

directory = "./data"
if not os.path.exists(directory):
    os.makedirs(directory)

df_campis = get_dataset(url=campis_url)
df_campis.to_csv(f"{directory}/df_cidades_campi.csv", index=False)

last_updated_date = []
last_updated_date.append(get_last_update_date(df_campis[df_campis["city"] == "Acarape"]))
last_updated_date.append(get_last_update_date(df_campis[df_campis["city"] == "Redenção"]))
last_updated_date.append(get_last_update_date(df_campis[df_campis["city"] == "São Francisco do Conde"]))

with open(f"{directory}/last_update_dates.csv", "w", encoding="utf-8") as csv_file:
    csv_writer= csv.writer(csv_file)
    csv_writer.writerow(["city", "dates"])
    for row in last_updated_date:
        city = row["city"]
        date = row["date"]
        csv_writer.writerow([
            city,
            date
        ])

df_rt = get_dataset(url=rt_url)
df_rt.to_csv(f"{directory}/df_cidades_rt.csv", index=False)