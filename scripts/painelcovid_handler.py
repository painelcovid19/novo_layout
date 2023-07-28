import time 
from get_accumulated_data import extract_and_load_acumulated_data
from get_df_cases import extract_and_load_df_cases
from get_macroregion_data import extract_and_load_macroregion_data


def painel_covid_etl(envent=5, respost=8):
    extract_and_load_df_cases()
    time.sleep(4)
    extract_and_load_acumulated_data()
    time.sleep(4)
    extract_and_load_macroregion_data()
    
if __name__ == "__main__":
    painel_covid_etl()