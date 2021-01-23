
import os # para acceder a la consola de python

# Importo el csv que contiene los datos de coches electricos mas limpios
import numpy as np
import pandas as pd
df= pd.read_csv('/home/tfm/Documentos/TFM/Datasets/CochesElectricos/coches electricos/ElectricCarData_Clean.csv', sep=',', encoding='unicode_escape', header=0)
type(df) # compruebo que sea dataFrame

# Comprobamos columnas y valores
df.columns 
df.values
type(df.values)

################################# 1. COMPROBAR CORRECTA TIPOLOGÍA Y ROL DE LAS VARIABLES #################################
df.dtypes # FastCharge no es una variable categorica sino numerica (entero)
type(df['FastCharge_KmH'])# se trata de una serie

# Convertimos FastCharge en variable de tipo numerico e indicando que queremos que convierta los valores erroneos en NA
# (errors='coerce') para que la conversion sea posible. De lo contrario, da error
df['FastCharge_KmH']= pd.to_numeric(df['FastCharge_KmH'],errors='coerce')
df['FastCharge_KmH'].values # Comprobamos que la fila donde habia un ('-') ha sido convertida a NA 
df['FastCharge_KmH']= df['FastCharge_KmH'].astype('Int64') # Convertimos la serie de float a enteros


#################################################### 2. EDA ###############################################################

# Analisis descriptivo basico de las variables numericas: comprobamos que todas toman valores coherentes. En principio,
# todos los valores parecen factibles sin sospechas de datos erroneos o valores perdidos.
df.describe()

# REPARTO DE FRECUENCIAS DE LAS VARIABLES CATEGORICAS

for i in df.columns.tolist():
    if df[i].dtype == 'O':
        print(f"\n\n LA TABLA DE FRECUENCIA DE {i} es: \n\n {df[i].value_counts()}")
print()

# Cuando se habla de conector Chademo, no veo que se diferencie entre tipo 1 y tipo 2 (mennekes). La unica diferencia entre
# Tipo1 y Tipo2 es que el Tipo2 admite una conexion trifasica. Por este motivo, recategorizo en una sola categoria.



# DISTINTOS VALORES EN CADA VARIABLE (detectar missing)
for i in df.columns.tolist():
        print(f"\n\n LOS DISTINTOS VALORES DE {i} son: \n\n {df[i].unique()}")
print()

# DETECTAR VALORES AUSENTES
df.filter(like='-', axis=0)
df.filter(like=' ', axis=0)
df.filter(like='na', axis=0)
df.filter(like= 'NA', axis=0)
df.filter(like='nan', axis=0)

# TRATAMIENTO VALORES MISSING
df.isnull().sum() #existen 5 valores ausentes en todo el dataframe. Todos estan en "FastCharge"

# EL procedimiento a seguir radica en:
# 1) comparar la fila que presente NA con el resto de filas del dataframe (2 a 2) y seleccionar 
# aquellas que tengan mayor numero de elementos en comun con dicha fila.



# BUCLE PARA IR RECORRIENDO TODAS LAS FILAS Y COMPARANDO

# EL problema es que los set no siguen un orden y, por tanto, hay valores que son coincidentes
# pero que corresponden a distintas variables

# Sin embargo, nos sirve para comparar de una manera inmediata los rasgos de los 5 coches que
# presentan la variable FastCharge ausente

for i in list(range(103)):
    fila1=set(list(df.iloc[57]))
    fila2=set(list(df.iloc[i]))
    final= fila1 & fila2
    if len(final) > 3 :
        print(f"Fila {i}")
        print("hay {} elementos coincidentes".format(len(final)))
        print(f" Los valores son: {final} \n")
print()

# Filtrar todos los coches entre 130 y 200 de autonomia porque parece que van a ser los mas
# parecidos al Renault y los Smart (comprobar)
filtroAutonomia= df[(df.Range_Km >=130) & (df.Range_Km<=200)] 
filtroAutonomia
type(filtroAutonomia) # se trata de un dataframe

# Dentro de "filtroAutonomia" aparecen los 2 Renault con NA. ELiminamos aquellas filas donde
# la marca sea Renault.
subfiltroAutonomia= filtroAutonomia[filtroAutonomia.Brand.str.contains("Renault")].index
filtroAutonomia= filtroAutonomia.drop(subfiltroAutonomia)
filtroAutonomia

filtroAutonomia['FastCharge_KmH']= pd.to_numeric(filtroAutonomia['FastCharge_KmH'])
filtroAutonomia['FastCharge_KmH']= filtroAutonomia['FastCharge_KmH'].astype('Int64') # Convertimos la serie de float a enteros
filtroAutonomia['FastCharge_KmH'].dtype

# 2) elegir de manera aleatoria el FastCharge de entre esas filas similares
import random

# FORMA 1
x = float("nan")
df['FastCharge_KmH'] = df['FastCharge_KmH'].apply(lambda x: random.choice(filtroAutonomia["FastCharge_KmH"].tolist()) if pd.isna(x) == True else x)

# FORMA 2
while(any(df.FastCharge_KmH == 'NA' is True)):
    df['FastCharge_KmH'] = df['FastCharge_KmH'] .fillna(random.choice(filtroAutonomia["FastCharge_KmH"].tolist())) 

# Comprobamos que se han rellenado aleatoriamente los 5 missing presentes en el dataframe 'df'

for i in [57,68,77,82,91]:
    a= df.iloc[i]
    print(a)
print()

# En resumen, imputar aleatoriamente el FastCharge ausente tomando como muestra los coches
# con caracteristicas similares.




# CORRECCION ERRORES DE ESCRITURA

# ELiminar caracteres en strings
df.columns = df.columns.str.strip() # elimina caracteres iniciales y finales                          
df.Model = df.Model.str.replace('-', '_') 
df.Model = df.Model.str.replace('!', '') 
df.Model = df.Model.str.replace('+', '') 
df.Model = df.Model.str.replace('.', '') 

# Convertir todos los campos de variables categoricas a mayusculas
for i in df.columns.tolist():
    if df[i].dtype == 'object':
        df[i] = df[i].str.upper()

df

# Convertir el nombre de todas las columnas a mayusculas
df.columns = df.columns.str.upper()


# ELIMINACION VARIABLES NO IMPORTANTES
df = df.drop(['PRICEEURO'], axis = 1)
df = df.drop(['SEGMENT'], axis = 1)
df = df.drop(['POWERTRAIN'], axis = 1)
df = df.drop(['ACCELSEC'], axis = 1)


df.columns



########################## 3.CREACION DE VARIABLES NUEVAS ###################################


