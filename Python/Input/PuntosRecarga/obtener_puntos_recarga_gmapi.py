# =============================================================================
# DESCARGA DATOS ESTACIONES DE RECARGA - GOOGLE MAPS PLACES API
# =============================================================================


"""
    Proceso: 


    Output: /home/tfm/Documentos/TFM/Datasets/PuntosRecarga/GoogleMapsAPI/
 
"""

# Se cargan las librerias
from datetime import datetime
import googlemaps
import os
import pandas as pd
import time


# API Google
gmaps = googlemaps.Client(key='Your API Key')


# Lista de las comunidades autónomas
comunidades = ["Aragon", "Andalucia", "Asturias", "Islas Baleares", "Canarias",
                "Cantabria", "Castilla-La Mancha", "Castilla y Leon", "Cataluña",
                "Comunidad Valenciana", "Extremadura", "Galicia", "Comunidad de Madrid",
                "La Rioja", "Murcia", "Navarra", "Pais Vasco"]


for comunidad in comunidades:

    SerchString = "estaciones de carga " + comunidad
    filename    = "puntos_carga_" + comunidad + ".csv"
    print(SerchString, filename)
    frames = []

    places_result = gmaps.places(query = SerchString,
                                 language = "es",
                                 region = "ES")

    df1 = pd.json_normalize(places_result["results"])
    frames.append(df1)

    if "next_page_token" in places_result:
        next_page_token = places_result["next_page_token"]
        time.sleep(10)  
        places_result_2 = gmaps.places(query = SerchString,
                                       language = "es",
                                       region = "ES",
                                       page_token=next_page_token)

        df2 = pd.json_normalize(places_result_2["results"])
        frames.append(df2)


        if "next_page_token" in places_result_2:
            next_page_token_2 = places_result_2["next_page_token"]
            time.sleep(10)
            places_result_3 = gmaps.places(query = SerchString,
                                           language = "es",
                                           region = "ES",
                                           page_token=next_page_token_2)
            df3 = pd.json_normalize(places_result_3["results"])
            frames.append(df3)

    result = pd.concat(frames)

    # Output
    filename = "puntos_carga_" + comunidad + ".csv"
    path = "/home/tfm/Documentos/TFM/Datasets/PuntosRecarga/GoogleMapsAPI/" + filename
    result.to_csv(path, index=False)  