###############MACHINE LEARNING ALGORITHM FOR GAS STATIONS IN SPAIN###############

#Import libraries
import datetime
import time
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib
plt.style.use("ggplot")
from matplotlib.pyplot import figure

matplotlib.rcParams["figure.figsize"] = (12,8)

#Import data into dataframe from csv
filename = "Gasolineras_de_España.csv"
path = "/home/tfm/Documentos/TFM/Datasets/" + filename
df = pd.read_csv(path)
print(df.shape)

#EDA (Exploratory Data Analysis)
df.head()
df.info()

#Numeric variables
df_numeric = df.select_dtypes(include='number')
df_numeric.info()
sns.displot(df_numeric["X"], bins=50, kde=True, rug=True)
sns.displot(df_numeric["Y"], bins=50, kde=True, rug=True)
sns.displot(df_numeric["FID"], bins=50, kde=True, rug=True)
sns.displot(df_numeric["objectid"], bins=50, kde=True, rug=True)
sns.displot(df_numeric["código_po"], bins=50, kde=True, rug=True)
sns.displot(df_numeric["longitud"], bins=50, kde=True, rug=True)
sns.displot(df_numeric["latitud"], bins=50, kde=True, rug=True)
sns.displot(df_numeric["precio_g_1"], bins=50, kde=True, rug=True)
sns.displot(df_numeric["precio_g_2"], bins=50, kde=True, rug=True)

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
plt.show(block=False)
time.sleep(5)
plt.close("all")

df_filt.info()
print(df_filt.shape)

print("End of script")