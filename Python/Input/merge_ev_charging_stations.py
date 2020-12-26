import pandas as pd
import matplotlib.pyplot as plt

#Mergear los csv de las distintas CCAA en un solo csv y volcarlo a un nuevo fichero
comunidades = ["Andalucia","Aragon","Asturias",
               "Cantabria","CastillaLaMancha","CastillayLeon",
                "Cataluña","ComunidadValenciana","Extremadura","Galicia",
                "ComunidaddeMadrid","LaRioja","Murcia","Navarra","PaisVasco"]
#Sin islas (ni Canarias ni Baleares)
frames = []
for comunidad in comunidades:
    filename = "puntos_carga_" + comunidad + ".csv"
    path = "/home/tfm/Documentos/TFM/Datasets/PuntosRecarga/GoogleMapsAPI/" + filename
    df = pd.read_csv(path)
    frames.append(df)
result = pd.concat(frames)
path_merged = "/home/tfm/Documentos/TFM/Datasets/PuntosRecarga/GoogleMapsAPI/puntos_carga_Espana.csv"
result.to_csv(path_merged, index=False)  

#Filtrar el dataframe para quedarnos solamente con las coordenadas

df_coord = result[["name","formatted_address","geometry.location.lat","geometry.location.lng"]]
df_coord.rename(columns={"geometry.location.lat": "latitude", "geometry.location.lng": "longitude"}, inplace=True)
print(df_coord.shape)
df_coord_filt = df_coord.query("longitude > -25 & latitude < 44")
print(df_coord_filt.shape)
BBox = ((df_coord_filt.longitude.min(), df_coord_filt.longitude.max(),      
         df_coord_filt.latitude.min(), df_coord_filt.latitude.max()))

path_filt = "/home/tfm/Documentos/TFM/Datasets/PuntosRecarga/puntos_carga_filt_Espana.csv"
df_coord_filt.to_csv(path_filt, index=False)  

espana = plt.imread("/home/tfm/Documentos/TFM/Datasets/PuntosRecarga/GoogleMapsAPI/espana.png")
fig, ax = plt.subplots(figsize = (8,7))
ax.scatter(df_coord_filt.longitude, df_coord_filt.latitude, zorder=1, alpha= 0.2, c='b', s=10)
ax.set_title('Plotting Spatial Data on Spain Map')
ax.set_xlim(BBox[0],BBox[1])
ax.set_ylim(BBox[2],BBox[3])
ax.imshow(espana, zorder=0, extent = BBox, aspect= 'equal')
plt.show()