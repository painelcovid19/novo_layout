import pandas as pd
import os
from graficos.packages.utils import get_datas, rename_city, columns, new_columns, remove_negatives
from graficos.packages.ibge_codes import codigosIBGE_CE, codigosIBGE_BA

df_cases = pd.read_csv("https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities.csv")

def extract_and_load_macroregion_data():
    
    all_codes = codigosIBGE_CE + codigosIBGE_BA
    datas = get_datas(all_codes, df_cases)

    macrorregions_data = pd.concat(datas)

    macrorregions_data = macrorregions_data[columns]

    macrorregions_data.columns = new_columns

    macrorregions_data["city"] = macrorregions_data["city"].apply(rename_city)

    macrorregion_CE = macrorregions_data[macrorregions_data["state"] == "CE"]
    macrorregion_BA = macrorregions_data[macrorregions_data["state"] == "BA"]

    macrorregion_CE.reset_index(drop=True, inplace=True)
    macrorregion_BA.reset_index(drop=True, inplace=True)


    macrorregion_CE = macrorregion_CE.sort_values(by="city", ignore_index=True)
    macrorregion_BA = macrorregion_BA.sort_values(by="city", ignore_index=True)


    s3_directory = "s3://painelcovid2023/data"

    macrorregion_CE.to_csv(f"{s3_directory}/df_dados_macro_regioes_ceara.csv", index=False)
    macrorregion_BA.to_csv(f"{s3_directory}/df_dados_macro_regioes_bahia.csv", index=False)
