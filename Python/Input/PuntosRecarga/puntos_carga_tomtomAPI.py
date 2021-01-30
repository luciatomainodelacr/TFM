# =============================================================================
#  INFORMACIÓN PUNTOS DE RECARGA - API TOMTOM
# =============================================================================

"""
    Fuente: https://developer.tomtom.com/search-api/search-api-documentation/ev-charging-stations-availability

    Proceso: Se carga el fichero puntos_carga_reduced_Espana.csv y mediante llamadas
    a la API de tomtom se recoge la información referente a los puntos de recarga:

    1- Clave API 
    2- Se define una función que haga la transacción a la url de cada punto y extraiga
    la info:
    - Se identifican los puntos por el id
    - Se introduce como input la latitud y longitud de cada punto
    - Se obtiene: nombre, dirección, provincia, ccaa, código postal, número de 
    conectores, potencia, tipo de conector
    - Se genera un diccionario con todas las variables
    3- Se aplica la función al dataframe generando una columna con el diccionario de las
    variables
    4- Split sobre la columna creada, generando las columnas para todas las variables
    5- Se exporta el dataframe a un fichero .csv

    Notas: Como máximo se pueden hacer al día un total de 2.500 transacciones a la API

    Input: /home/tfm/Documentos/TFM/Datasets/puntos_carga_reduced_Espana.csv
    Output: /home/tfm/Documentos/TFM/Datasets/ptos_recarga_info.csv
"""


# Se cargan las librerias
import os
import requests
import json
import pandas as pd

# Se establece el diretorio base
os.chdir('/home/tfm/Documentos/TFM/Datasets/')

# API KEY - Tomtom
api_key = 'vBGAofG9iufITkNwekDkGA9xjAoEmM9o' 
category = 'estaciones de carga de vehículos eléctricos'



# 1.- Carga de inputs ---------------------------------------------
#------------------------------------------------------------------

# Puntos de recarga
df = pd.read_csv(os.path.join(os.getcwd(),'PuntosRecarga/puntos_carga_reduced_Espana.csv'), sep = ',', encoding = 'iso-8859-1', decimal = '.')

# Selección de las variables
df = df[["id", "latitude", "longitude"]]



# 2.- Función API Búsqueda ----------------------------------------
#------------------------------------------------------------------

def tomtom_category_search_request(api_key, category, id_pto, lat_pto, long_pto):
    
    # Se define la url para cada par (lat, long)
    url = """
            https://api.tomtom.com/search/2/categorySearch/{category}.json?key={api_key}&countrySet=ES&lat={lat_pto}&lon={long_pto}
          """.format(category=category, api_key=api_key, lat_pto= lat_pto, long_pto= long_pto)
    

    # Se extrae la información del fichero json
    response = requests.get(url)
    data = response.json()
   
    number_pois = len(data["results"])
    poi_data = {}


    # Se extrae información necesaria
    for result in data["results"]:
        name = result["poi"]["name"] if "name" in result["poi"] else None

        # Campos adress
        streetName  = result["address"]["streetName"] if "streetName" in result["address"] else None
        provincia   = result["address"]["countrySecondarySubdivision"] if "countrySecondarySubdivision" in result["address"] else None
        ccaa        = result["address"]["countrySubdivision"] if "countrySubdivision" in result["address"] else None
        postalCode  = result["address"]["postalCode"] if "postalCode" in result["address"] else None

        # Campos chargingPark 
        if "chargingPark" in result and result["chargingPark"] != {}: 
            num_connectors = len(result["chargingPark"]["connectors"]) if "connectors" in result["chargingPark"] else None
            
            if num_connectors > 1:
                connectorType = [j["connectorType"] if "connectorType" in j else None for j in result["chargingPark"]["connectors"]] 
                ratedPowerKW  = [j["ratedPowerKW"] if "ratedPowerKW" in j else None for j in result["chargingPark"]["connectors"]] 
                
            else:
                connectorType = [j["connectorType"] for j in result["chargingPark"]["connectors"]][0] if "connectorType" in result["chargingPark"]["connectors"][0] else None
                ratedPowerKW  = [j["ratedPowerKW"] for j in result["chargingPark"]["connectors"]][0] if "ratedPowerKW" in result["chargingPark"]["connectors"][0] else None

        else:
            num_connectors = 'no disponible'
            connectorType  = 'no disponible'
            ratedPowerKW   = 'no disponible'
            
            
    # Se define el json resultado
    poi_data = {
        "name"          : name,
        "streetName"    : streetName,
        "provincia"     : provincia,
        "ccaa"          : ccaa,
        "postalCode"    : postalCode,
        "connectorType" : connectorType,
        "ratedPowerKW"  : ratedPowerKW,
        "num_connectors": num_connectors
    }

    return poi_data




# 3.- Se aplica la función al dataframe ---------------------------
#------------------------------------------------------------------

# Se generan una columna con un diccionario con todas las variables
df["poi_data"]  = df.apply(lambda a: tomtom_category_search_request(api_key, category, a["id"], a["latitude"], a["longitude"]), axis = 1)

# Split de los diccionarios generando las nuevas variables
df = pd.concat([df.drop(["poi_data"], axis = 1), df["poi_data"].apply(pd.Series)], axis = 1)



# 4.- Output ------------------------------------------------------
#------------------------------------------------------------------

df.to_csv('/home/tfm/Documentos/TFM/Datasets/PuntosRecarga/ptos_recarga_info.csv', sep = ";", index = False)