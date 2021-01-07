###############MACHINE LEARNING ALGORITHM FOR GAS STATIONS IN SPAIN###############

#Import libraries
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

#FUNCTIONS
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

if __name__ == "__main__":
    #Import data into dataframe from csv
    filename = "Gasolineras_de_España.csv"
    path = "/home/tfm/Documentos/TFM/Datasets/" + filename
    df = pd.read_csv(path)
    print(df.shape)

    #EDA (Exploratory Data Analysis)
    df.head()
    df.info()

    #Numeric variables
    df_numeric = df.select_dtypes(include="number")
    df_numeric.info()
    plot_multiple_histograms(df_numeric, ["X","Y","FID","objectid","código_po","longitud","latitud","precio_g_1","precio_g_2"])
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
    df_filt = df.query("longitud > -10 & latitud > 34 & provincia != 'BALEARS (ILLES)'")

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

    with open("/home/tfm/Documentos/TFM/Datasets/categorical.txt", "w") as f:
        for column in df_non_numeric:
            print(df_non_numeric[column].value_counts(), file=f)
    
    df_filt.drop(df.filter(regex="precio").columns, axis="columns", inplace=True)
    df_filt.info()
    print("End of script")