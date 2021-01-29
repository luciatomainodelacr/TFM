# =============================================================================
#  INFORMACIÓN PUNTOS DE RECARGA
# =============================================================================


# Se cargan las librerias
import os
import requests
import json
import pandas as pd

# Se establece el diretorio base
os.chdir('/home/tfm/Documentos/TFM/Datasets/')

# API KEY - Tomtom
api_key = 'vBGAofG9iufITkNwekDkGA9xjAoEmM9o' 


# 1.- Carga de inputs ---------------------------------------------
#------------------------------------------------------------------

# Puntos de recarga
df = pd.read_csv(os.path.join(os.getcwd(),'PuntosRecarga/puntos_carga_reduced_Espana.csv'), sep = ',', encoding = 'iso-8859-1', decimal = '.')


# 2.- Función API Búsqueda ----------------------------------------
#------------------------------------------------------------------

def tomtom_category_search_request(api_key, category, lat_pto, long_pto, id_pto):
    
    url = """
            https://api.tomtom.com/search/2/categorySearch/{category}.json?key={api_key}&countrySet=ES&lat={lat_pto}&lon={long_pto}
          """.format(category=category, api_key=api_key, lat_pto= lat_pto, long_pto= long_pto)
    
    response = requests.get(url)
    data = response.json()
   
    number_pois = len(data['results'])
    poi_data = {}


    # Se extrae información necesaria
    for result in data['results']:
        name = result["poi"]["name"] if "name" in result["poi"] else None

        # Campos adress
        streetName = result["address"]["streetName"] if "streetName" in result["address"] else None
        provincia = result["address"]["countrySecondarySubdivision"] if "countrySecondarySubdivision" in result["address"] else None
        ccaa = result["address"]["countrySubdivision"] if "countrySubdivision" in result["address"] else None
        postalCode = result["address"]["postalCode"] if "postalCode" in result["address"] else None
        
        

        # Campos chargingPark 
        if "chargingPark" in result and result["chargingPark"] != {}: 
            num_connectors = len(result["chargingPark"]["connectors"]) if "connectors" in result["chargingPark"] else None

            
            if num_connectors > 1:
                connectorType = [j["connectorType"] if "connectorType" in j else None for j in result["chargingPark"]["connectors"]] 
                ratedPowerKW = [j["ratedPowerKW"] if "ratedPowerKW" in j else None for j in result["chargingPark"]["connectors"]] 
                
            else:
                connectorType = [j["connectorType"] for j in result["chargingPark"]["connectors"]][0] if "connectorType" in result["chargingPark"]["connectors"][0] else None
                ratedPowerKW = [j["ratedPowerKW"] for j in result["chargingPark"]["connectors"]][0] if "ratedPowerKW" in result["chargingPark"]["connectors"][0] else None
        

        else:
            num_connectors = "no disponible"
            connectorType = "no disponible"
            ratedPowerKW = "no disponible"
            
            
            # Se define el json resultado
    poi_data[id_pto] = {
        'name': name,
        'streetName': streetName,
        'provincia': provincia,
        'ccaa': ccaa,
        'postalCode': postalCode,
        'connectorType': connectorType,
        'ratedPowerKW': ratedPowerKW,
        'num_connectors': num_connectors
    }


    return {"data": poi_data, "number_pois": number_pois}




# 5.- Obtener ID puntos de recarga -----------------------------------------------------
#------------------------------------------------------------------

# Se inicializa una lista vacia para calcular las distancias
list_id_pto = []
list_latitude = []
list_longitude = []
list_name = []
list_streetName = []
list_provincia = []
list_ccaa = []
list_postalCode = []
list_connectorType = []
list_ratedPowerKW = []
list_num_connectors = []


# Bucle que guarde en las listas la información para cada punto de recarga de nuestro dataframe
for i in df.index:

    id_pto = df['id'][i]
    lat_pto = df['latitude'][i]
    long_pto = df['longitude'][i]

    # Llamada a la funcion API busqueda
    result = tomtom_category_search_request(api_key, 'estaciones de carga de vehículos eléctricos', lat_pto, long_pto, id_pto)

    # Variables para la información de cada punto
    name = result['data'][id_pto]['name']
    streetName = result['data'][id_pto]['streetName']
    provincia = result['data'][id_pto]['provincia']
    ccaa = result['data'][id_pto]['ccaa']
    postalCode = result['data'][id_pto]['postalCode']

    connectorType = result['data'][id_pto]['connectorType']
    ratedPowerKW = result['data'][id_pto]['ratedPowerKW']
    num_connectors = result['data'][id_pto]['num_connectors']


    # Se apendiza a las listas creadas
    list_id_pto.append(id_pto)
    list_latitude.append(lat_pto)
    list_longitude.append(long_pto)
    list_name.append(name)
    list_streetName.append(streetName)
    list_provincia.append(provincia)
    list_ccaa.append(ccaa)
    list_postalCode.append(postalCode)
    list_connectorType.append(connectorType)
    list_ratedPowerKW.append(ratedPowerKW)
    list_num_connectors.append(num_connectors)




# Se crea un dataframe con la información resultante
df_ptos_recarga_final = pd.DataFrame()

df_ptos_recarga_final['id'] = list_id_pto
df_ptos_recarga_final['latitude'] = list_latitude
df_ptos_recarga_final['longitude'] = list_longitude
df_ptos_recarga_final['name'] = list_name
df_ptos_recarga_final['streetName'] = list_streetName
df_ptos_recarga_final['provincia'] = list_provincia
df_ptos_recarga_final['ccaa'] = list_ccaa
df_ptos_recarga_final['postalCode'] = list_postalCode
df_ptos_recarga_final['connectorType'] = list_connectorType
df_ptos_recarga_final['ratedPowerKW'] = list_ratedPowerKW
df_ptos_recarga_final['num_connectors'] = list_num_connectors




# 5.- Output ------------------------------------------------------
#------------------------------------------------------------------

df_ptos_recarga_final.to_csv('/home/tfm/Documentos/TFM/Datasets/PuntosRecarga/ptos_recarga_info.csv', sep = ";", index = False)