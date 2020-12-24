import pandas as pd

comunidades = ["Andalucia","Aragon","Asturias","IslasBaleares","Canarias",
               "Cantabria","CastillaLaMancha","CastillayLeon",
                "Cataluña","ComunidadValenciana","Extremadura","Galicia",
                "ComunidaddeMadrid","LaRioja","Murcia","Navarra","PaisVasco"]
frames = []
for comunidad in comunidades:
    filename = "puntos_carga_" + comunidad + ".csv"
    path = "/home/tfm/Documentos/TFM/Datasets/GoogleMapsAPI/" + filename
    df = pd.read_excel(path)
    frames.append(df)
result = pd.concat(frames)