# =============================================================================
#  PUNTOS DE RECARGAS ESPAÑA
# =============================================================================


# Se cargan las librerias
import sys
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import operator

from sklearn.cluster import DBSCAN
from geopy.distance import great_circle
from shapely.geometry import MultiPoint

# Desactivar warnings
pd.options.mode.chained_assignment = None  # default='warn'

#FUNCTIONS
def extraer_provincia(lugares, formatted_address):
    x = ''
    for j in lugares:
        if j in formatted_address:
            x  = j 

        if x == 'Benahadux':
            x = 'Almería'

        if x == 'Santiago de Compostela' or x == 'Esclavitud' or x == 'Narón':
            x = 'A Coruña'

        if x == 'Illes Balears':
            x = 'Baleares'

        if x == 'Martorell' or x == 'Pedraforca' or x == 'Mas Roca':
            x = 'Barcelona'

        if x == 'Ambrosero' or x == 'Vega Reinosa':
            x = 'Cantabria' 

        if x == 'Belmonte' or x == 'Atalaya del Cañavate':
            x = 'Cuenca'

        if x == 'Cdad. Real':
            x = 'Ciudad Real'

        if x == 'Gipuzkoa' or x == 'Donostia' or x == 'SS':
            x = 'Guipúzcoa'
        
        if x == 'Girona':
            x = 'Gerona'

        if x == 'Trijueque':
            x = 'Guadalajara'

        if x == 'Tricio' or x == 'El Villar de Arnedo':
            x = 'La Rioja'        

        if x == 'Bembibre':
            x = 'León'

        if x == '28946':
            x = 'Madrid'

        if x == 'Marbella':
            x = 'Málaga'

        if x == 'Lorca' or x == 'Diseminado Salinas' or x == '30110' or x == '30848':
            x = 'Murcia'

        if x == 'Navarre' or x == 'Tudela' or x == 'Leitza' or x == 'Azagra' or x == 'Imárcoain':
            x = 'Navarra'

        if x == 'PO':
            x = 'Pontevedra'

        if x == '41012':
            x = 'Sevilla'

        if x == 'Oropesa' or x == 'Ocaña':
            x = 'Toledo'

        if x == 'Portugalete' or x == 'BI' or x == 'Bizkaia' or x == 'Leioa':
            x = 'Vizcaya'

        if x == 'València' or x == '46370' or x == 'Carcagente':
            x = 'Valencia'

        if x == 'Gasteiz' or x == 'Araba':
            x = 'Álava'

    return x

def extraer_cp(formatted_address):
    result = ''
    x = [int(s) for s in formatted_address.split() if s.isdigit()]

    if len(x) == 0:
        result = 'No_infor'

    if len(x) == 1 and len(str(x[0])) == 5:
        result = x[0]

    if len(x) == 2 and len(str(x[0])) == 5:
        result = x[0]
        
    if len(x) == 2 and len(str(x[1])) == 5:
        result = x[1]

    return result

def get_centermost_point(cluster):
        centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
        centermost_point = min(cluster, key=lambda point: great_circle(point, centroid).m)
        return tuple(centermost_point)

def clustering_dbscan(df_filt):
    coords = df_filt[["latitude", "longitude"]].values
    kms_per_radian = 6371.0088
    epsilon = 5 / kms_per_radian
    db = DBSCAN(eps=epsilon, min_samples=2, algorithm="ball_tree", metric="haversine").fit(np.radians(coords))
    cluster_labels = db.labels_
    num_clusters = len(set(cluster_labels))
    clusters = pd.Series([coords[cluster_labels == n] for n in range(num_clusters-1)])
    print("Number of clusters: {}".format(num_clusters))

    centermost_points = clusters.map(get_centermost_point)
    lats, lons = zip(*centermost_points)
    rep_points = pd.DataFrame({"longitude":lons, "latitude":lats})
    rs = rep_points.apply(lambda row: df_filt[(df_filt["latitude"]==row["latitude"]) & (df_filt["longitude"]==row["longitude"])].iloc[0], axis=1)
    return rs

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("ERROR: This program needs at least 2 parameters: program_name program_type")
        sys.exit(1)
    else:
        print("The number of arguments is ", len(sys.argv))
        program_name = sys.argv[0]
        # program type can be: "FILTER", "REDUCE", "ALL"
        program_type = sys.argv[1]
        print("The program run is: ",program_name, program_type)

    path_filt = "/home/tfm/Documentos/TFM/Datasets/PuntosRecarga/puntos_carga_filt_Espana.csv"
    path_merged = "/home/tfm/Documentos/TFM/Datasets/PuntosRecarga/GoogleMapsAPI/puntos_carga_Espana.csv"
    path_reduced = "/home/tfm/Documentos/TFM/Datasets/PuntosRecarga/puntos_carga_reduced_Espana.csv"
    if program_type != "REDUCE":
        # 1.- Union puntos de recarga por CCAA ----------------------------
        #------------------------------------------------------------------

        # Mergear los csv de las distintas CCAA en un solo csv y volcarlo a un nuevo fichero
        comunidades = ["Andalucia","Aragon","Asturias",
                        "Cantabria","CastillaLaMancha","CastillayLeon",
                        "Cataluña","ComunidadValenciana","Extremadura","Galicia",
                        "ComunidaddeMadrid","LaRioja","Murcia","Navarra","PaisVasco"]
        # Sin islas (ni Canarias ni Baleares)
        frames = []
        for comunidad in comunidades:
            filename = "puntos_carga_" + comunidad + ".csv"
            path = "/home/tfm/Documentos/TFM/Datasets/PuntosRecarga/GoogleMapsAPI/" + filename
            df = pd.read_csv(path)
            frames.append(df)
        result = pd.concat(frames)
        result.to_csv(path_merged, index=False)  

        # 2.- Filtrar el dataframe para quedarnos solamente con las coordenadas -----------------------------------------
        #------------------------------------------------------------------
        
        df_coord = result[["name","formatted_address","geometry.location.lat","geometry.location.lng"]]
        df_coord.rename(columns={"geometry.location.lat": "latitude", "geometry.location.lng": "longitude"}, inplace=True)
        print(df_coord.shape)
        df_coord_filt = df_coord.query("longitude > -25 & latitude < 44")
        print(df_coord_filt.shape)
        BBox = ((df_coord_filt.longitude.min(), df_coord_filt.longitude.max(),      
                 df_coord_filt.latitude.min(), df_coord_filt.latitude.max()))

        # 3.- Grafico mapa España -----------------------------------------
        #------------------------------------------------------------------

        espana = plt.imread("/home/tfm/Documentos/TFM/Datasets/PuntosRecarga/GoogleMapsAPI/espana.png")
        fig, ax = plt.subplots(figsize = (8,7))
        ax.scatter(df_coord_filt.longitude, df_coord_filt.latitude, zorder=1, alpha= 0.2, c='b', s=10)
        ax.set_title('Plotting Spatial Data on Spain Map')
        ax.set_xlim(BBox[0],BBox[1])
        ax.set_ylim(BBox[2],BBox[3])
        ax.imshow(espana, zorder=0, extent = BBox, aspect= 'equal')
        # plt.show()

        # 4.- Extraer provincia -------------------------------------------
        #------------------------------------------------------------------

        df = df_coord_filt.drop_duplicates()

        lugares = ['A Coruña', 'Álava', 'Albacete', 'Alicante', 'Almería', 'Ambrosero',
        'Araba', 'Asturias', 'Atalaya del Cañavate', 'Ávila', 'Azagra', 'Badajoz',
        'Baleares', 'Barcelona', 'Bembibre', 'Belmonte', 'Benahadux', 'BI', 'Bizkaia',
        'Burgos', 'Cáceres', 'Cádiz', 'Cantabria', 'Carcagente', 'Castellón', 'Ceuta',
        'Ciudad Real', 'Cdad. Real', 'Córdoba', 'Cuenca', 'Diseminado Salinas',
        'El Villar de Arnedo', 'Esclavitud', 'Gasteiz', 'Gerona', 'Girona', 'Granada',
        'Guadalajara', 'Guipúzcoa', 'Gipuzkoa', 'Huelva', 'Huesca', 'Illes Balears',
        'Imárcoain', 'Jaén', 'La Rioja', 'Las Palmas', 'León', 'Leioa', 'Leitza',
        'Lleida', 'Lorca', 'Lugo', 'Madrid',  'Málaga', 'Marbella', 'Martorell',
        'Mas Roca', 'Melilla', 'Murcia', 'Narón', 'Navarra', 'Navarre', 'Ocaña',
        'Ourense', 'Oropesa', 'Palencia', 'Pedraforca', 'PO', 'Pontevedra', 'Portugal',
        'Portugalete', 'SS', 'S.C. Tenerife', 'Salamanca', 'Santiago de Compostela',
        'Segovia', 'Sevilla', 'Soria', 'Tarragona', 'Teruel', 'Toledo', 'Tricio',
        'Trijueque', 'Tudela', 'Valencia', 'València', 'Valladolid', 'Vega Reinosa',
        'Vizcaya', 'Zamora', 'Zaragoza', '28946', '30110', '30848', '41012', '46370']

        df["province"] = df.apply(lambda a: extraer_provincia(lugares, a['formatted_address']), axis = 1)

        # Se comprueba cuantos valores quedan sin informar
        list(df['province']).count('')

        # Se filtran eliminando Portugal y Baleares
        df = df[df['province'] != 'Portugal']
        df = df[df['province'] != 'Baleares']

        # Se grafican de nuevo los puntos
        espana = plt.imread("/home/tfm/Documentos/TFM/Datasets/PuntosRecarga/GoogleMapsAPI/espana.png")
        fig, ax = plt.subplots(figsize = (8,7))
        ax.scatter(df.longitude, df.latitude, zorder = 1, alpha = 0.2, c = 'b', s = 10)
        ax.set_title('Plotting Spatial Data on Spain Map')
        ax.set_xlim(BBox[0], BBox[1])
        ax.set_ylim(BBox[2], BBox[3])
        ax.imshow(espana, zorder = 0, extent = BBox, aspect = 'equal')
        plt.show()

        # 5.- Extraer codigo postal ---------------------------------------
        #------------------------------------------------------------------
        df["cp"] = df.apply(lambda a: extraer_cp(a['formatted_address']), axis = 1)

        # 6.- Output ------------------------------------------------------
        #------------------------------------------------------------------

        # Dataframe resultante
        df.to_csv(path_filt, sep = ";", index = False)


    if program_type != "FILTER":
        #Importar csv fitrado a df_filt
        df_filt = pd.read_csv(path_filt, sep=";")
        print(df_filt.shape)
        print(df_filt.province.unique())
        dict_CCAA = {}
        for provincia in df_filt.province.unique():
            dict_CCAA[provincia] = df_filt[df_filt["province"] == provincia].shape
        sort_CCAA = sorted(dict_CCAA.items(), key=operator.itemgetter(1), reverse=True)
        print(sort_CCAA)
        # 7.- Filtrar por CCAA---------------------------------------------
        #------------------------------------------------------------------
        # Vamos a filtrar los datos con un algoritmo de Clustering DBSCAN
        # , que reduce la dimensión de manera geográficamente uniforme 
        frames = []
        provincias_muchos_puntos = ["Madrid","Valencia","Navarra","Murcia","Asturias","Cantabria","Barcelona"]
        for provincia in df_filt.province.unique():
            df_CCAA = df_filt[df_filt["province"] == provincia]
            print(provincia, df_CCAA.shape)
            if provincia in provincias_muchos_puntos:
                #Clustering to reduce spatial dataset size with DBSCAN
                #Source: https://geoffboeing.com/2014/08/clustering-to-reduce-spatial-data-set-size/
                print("Clustering with DBSCAN")
                rs = clustering_dbscan(df_CCAA)
                fig, ax = plt.subplots(figsize=[10, 6])
                rs_scatter = ax.scatter(rs["longitude"], rs["latitude"], c="#99cc99", edgecolor="None", alpha=0.7, s=120)
                df_scatter = ax.scatter(df_CCAA["longitude"], df_CCAA["latitude"], c="k", alpha=0.9, s=3)
                ax.set_title("Full data set vs DBSCAN reduced set")
                ax.set_xlabel("Longitude")
                ax.set_ylabel("Latitude")
                ax.legend([df_scatter, rs_scatter], ["Full set", "Reduced set"], loc="upper right")
                plt.show()
            else:
                rs = df_CCAA
            frames.append(rs)
        result = pd.concat(frames)
        #Export reduced dataframe to csv
        result.drop("cp",axis="columns", inplace=True)
        result.to_csv(path_reduced, index=False) 
        print("Exported reduced dataframe with ",result.shape," to ",path_reduced)
        
    print("End of script")