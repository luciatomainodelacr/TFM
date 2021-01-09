###############MACHINE LEARNING ALGORITHM FOR GAS STATIONS IN SPAIN###############

#Import libraries
import sys
import datetime
import time
import math
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib
plt.style.use("ggplot")
from matplotlib.pyplot import figure

matplotlib.rcParams["figure.figsize"] = (12,8)
import unidecode

from sklearn.cluster import DBSCAN
from geopy.distance import great_circle
from shapely.geometry import MultiPoint

#FUNCTIONS
def remove_accents(a):
    #return unidecode.unidecode(a.decode('utf-8'))
    return unidecode.unidecode(a)

def plot_multiple_histograms(df, cols):
    num_plots = len(cols)
    num_cols = math.ceil(np.sqrt(num_plots))
    num_rows = math.ceil(num_plots/num_cols)
        
    fig, axs = plt.subplots(num_rows, num_cols)
    
    for ind, col in enumerate(cols):
        i = math.floor(ind/num_cols)
        j = ind - i*num_cols
            
        if num_rows == 1:
            if num_cols == 1:
                sns.histplot(df[col], kde=True, ax=axs)
            else:
                sns.histplot(df[col], kde=True, ax=axs[j])
        else:
            sns.histplot(df[col], kde=True, ax=axs[i, j])

def plot_multiple_countplots(df, cols):
    num_plots = len(cols)
    num_cols = math.ceil(np.sqrt(num_plots))
    num_rows = math.ceil(num_plots/num_cols)
        
    fig, axs = plt.subplots(num_rows, num_cols)
    
    for ind, col in enumerate(cols):
        i = math.floor(ind/num_cols)
        j = ind - i*num_cols
        
        if num_rows == 1:
            if num_cols == 1:
                sns.countplot(x=df[col], ax=axs)
            else:
                sns.countplot(x=df[col], ax=axs[j])
        else:
            sns.countplot(x=df[col], ax=axs[i, j])

def exploratory_data_analysis(df):
    df.head()
    df.info()

    #Remove accents and other special characters
    for column in ["provincia","municipio","localidad","direccion","rotulo"]:
        df[column] = df[column].apply(remove_accents)

    #Numeric variables
    df_numeric = df.select_dtypes(include="number")
    df_numeric.info()
    plot_multiple_histograms(df_numeric, ["X","Y","FID","objectid","codigo_po","longitud","latitud","precio_g_1","precio_g_2"])
    plt.show()
    time.sleep(15)
    plt.close("all")

    comparison_column_1 = np.where(df["longitud"] == df["X"], True, False)
    if np.all(comparison_column_1):
        print("Longitud igual a X")
    else:
        print("Longitud NO es igual a X")
    
    comparison_column_2 = np.where(df["latitud"] == df["Y"], True, False)
    if np.all(comparison_column_2):
        print("Latitud igual a Y")
    else:
        print("Latitud NO es igual a Y")

    df.drop("X",axis="columns", inplace=True)
    df.drop("Y",axis="columns", inplace=True)

    # Filter coordinates value for Peninsular Spain
    df_filt = df.query("longitud > -10 & latitud > 34 & provincia != 'BALEARS (ILLES)' & provincia != 'MELILLA' & provincia != 'CEUTA'")

    print(df_filt["provincia"].unique())
    sns.displot(df_filt["longitud"], bins=50, kde=True, rug=True)
    sns.displot(df_filt["latitud"], bins=50, kde=True, rug=True)
    #plt.show(block=False)
    #time.sleep(5)
    #plt.close("all")

    df_filt.info()
    print(df_filt.shape)

    plot_multiple_histograms(df_filt, ["latitud","longitud"])
    plt.show()
    time.sleep(30)
    plt.close("all")

    #Categorical variables
    df_non_numeric = df_filt.select_dtypes(exclude="number")
    df_non_numeric.info()

    plt.figure(figsize=(25,7))
    sns.countplot(x="provincia",
                data=df_non_numeric)
    plt.show()
    time.sleep(15)
    plt.close("all")

    with open("/home/tfm/Documentos/TFM/Datasets/Gasolineras/gas_stations_categorical.txt", "w") as f:
        for column in df_non_numeric:
            print(df_non_numeric[column].value_counts(), file=f)
    
    df_filt.drop(df.filter(regex="precio").columns, axis="columns", inplace=True)
    df_filt.drop("horario00",axis="columns", inplace=True)
    df_filt.drop("z",axis="columns", inplace=True)
    df_filt.drop("fecha",axis="columns", inplace=True)
    df_filt.drop(df.filter(regex="f_").columns, axis="columns", inplace=True)
    df_filt.drop("objectid",axis="columns", inplace=True)
    df_filt.drop("FID",axis="columns", inplace=True)
    df_filt.info()
    return df_filt

def get_centermost_point(cluster):
        centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
        centermost_point = min(cluster, key=lambda point: great_circle(point, centroid).m)
        return tuple(centermost_point)

def clustering_dbscan(df_filt):
    coords = df_filt[["latitud", "longitud"]].values
    kms_per_radian = 6371.0088
    epsilon = 5 / kms_per_radian
    db = DBSCAN(eps=epsilon, min_samples=2, algorithm="ball_tree", metric="haversine").fit(np.radians(coords))
    cluster_labels = db.labels_
    num_clusters = len(set(cluster_labels))
    clusters = pd.Series([coords[cluster_labels == n] for n in range(num_clusters-1)])
    print("Number of clusters: {}".format(num_clusters))

    centermost_points = clusters.map(get_centermost_point)
    lats, lons = zip(*centermost_points)
    rep_points = pd.DataFrame({"longitud":lons, "latitud":lats})
    rs = rep_points.apply(lambda row: df_filt[(df_filt["latitud"]==row["latitud"]) & (df_filt["longitud"]==row["longitud"])].iloc[0], axis=1)
    return rs

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("ERROR: This program needs at least 2 parameters: program_name program_type")
        sys.exit(1)
    else:
        print("The number of arguments is ", len(sys.argv))
        program_name = sys.argv[0]
        # program type can be: "EDA", "CLUSTER", "ALL"
        program_type = sys.argv[1]
        print("The program run is: ",program_name, program_type)

    path = "/home/tfm/Documentos/TFM/Datasets/Gasolineras/Gasolineras_de_España.csv"
    path_filt = "/home/tfm/Documentos/TFM/Datasets/Gasolineras/gasolineras_filt_Espana.csv"
    path_reduced = "/home/tfm/Documentos/TFM/Datasets/Gasolineras/gasolineras_reduced_Espana.csv"
    if program_type != "CLUSTER":
        #Import data into dataframe from csv
        df = pd.read_csv(path)
        print("Imported dataframe from ",path," with ",df.shape)

        #EDA
        print("Exploratory Data Analysis and generation of gasolineras_filt_Espana.csv")
        df_filt = exploratory_data_analysis(df)  

        #Export dataframe to filtered csv
        df_filt.to_csv(path_filt, index=False) 
        print("Exported filtered dataframe with ",df_filt.shape," to ",path_filt)
    
    if program_type != "EDA":
        #Import filtered data into dataframe from csv
        df_filt = pd.read_csv(path_filt)
        print("Imported filtered dataframe from ",path_filt," with ",df_filt.shape)
        
        #Clustering to reduce spatial dataset size with DBSCAN
        #Source: https://geoffboeing.com/2014/08/clustering-to-reduce-spatial-data-set-size/
        print("Clustering with DBSCAN")
        rs = clustering_dbscan(df_filt)
        fig, ax = plt.subplots(figsize=[10, 6])
        rs_scatter = ax.scatter(rs["longitud"], rs["latitud"], c="#99cc99", edgecolor="None", alpha=0.7, s=120)
        df_scatter = ax.scatter(df_filt["longitud"], df_filt["latitud"], c="k", alpha=0.9, s=3)
        ax.set_title("Full data set vs DBSCAN reduced set")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.legend([df_scatter, rs_scatter], ["Full set", "Reduced set"], loc="upper right")
        plt.show()

        #Export reduced dataframe to csv
        rs.to_csv(path_reduced, index=False) 
        print("Exported reduced dataframe with ",rs.shape," to ",path_reduced)
    print("End of script")