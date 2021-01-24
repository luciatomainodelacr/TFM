
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

########################## TRATAMIENTO VALORES MISSING ########################################

df.isnull().sum() #existen 5 valores ausentes en todo el dataframe. Todos estan en "FastCharge"
# Podemos optar por imputar esos valores o ponerlos a cero, segun la interpretacion



# PROCEDIMIENTO PARA IMPUTAR LOS VALORES AUSENTES DE FASTCHARGE

'''EL procedimiento a seguir radica en:
1) comparar la fila que presente NA con el resto de filas del dataframe (2 a 2) y seleccionar 
aquellas que tengan mayor numero de elementos en comun con dicha fila.

BUCLE PARA IR RECORRIENDO TODAS LAS FILAS Y COMPARANDO

EL problema es que los set no siguen un orden y, por tanto, hay valores que son coincidentes
pero que corresponden a distintas variables

Sin embargo, nos sirve para comparar de una manera inmediata los rasgos de los 5 coches que
presentan la variable FastCharge ausente'''

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

# Comprobamos que se han rellenado aleatoriamente los 5 missing presentes en el dataframe 'df'

for i in [57,68,77,82,91]:
    a= df.iloc[i]
    print(a)
print()

# En resumen, imputar aleatoriamente el FastCharge ausente tomando como muestra los coches
# con caracteristicas similares.



''' ASIGNAR EL VALOR '0' A LOS 5 VALORES AUSENTES PUESTO QUE QUIERE DECIR QUE ESOS 5 COCHES NO 
PRESENTAN OPCION A FASTCHARGE'''

df = df.fillna(0)
df.isnull().sum() # comprobamos que se han asignado correctamente 
for i in [57,68,77,82,91]:
    a= df.iloc[i]
    print(a)
print()




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


''' *****************Estrucuturas los tipos de conectores en listas********************'''

'''LOS DISTINTOS VALORES DE PLUGTYPE son: ['TYPE 2 CCS' 'TYPE 2 CHADEMO' 'TYPE 2' 'TYPE 1 CHADEMO']'''

df['PLUGTYPE'] = df['PLUGTYPE'].replace({'TYPE 2':'TYPE2'})
df['PLUGTYPE'] = df['PLUGTYPE'].replace({'TYPE 2 CCS':'TYPE2,CCS'})
df['PLUGTYPE'] = df['PLUGTYPE'].replace({'TYPE 2 CHADEMO':'TYPE2,CHADEMO'})
df['PLUGTYPE'] = df['PLUGTYPE'].replace({'TYPE 1 CHADEMO':'TYPE1,CHADEMO'})

df.PLUGTYPE.values[0][1] # acceder a cada elemento de la lista

# Funcion para convertir un string separado por comas en elementos de una lista
def convertir(string):
    li = list(string.split(","))
    return li

# Mapeamos cada elemento de la columna aplicando la funcion convertir
df.PLUGTYPE = list(map(convertir, df.PLUGTYPE.values.tolist()))




# ELIMINACION VARIABLES NO IMPORTANTES
df = df.drop(['PRICEEURO'], axis = 1)
df = df.drop(['SEGMENT'], axis = 1)
df = df.drop(['POWERTRAIN'], axis = 1)
df = df.drop(['ACCELSEC'], axis = 1)
df = df.drop(['TOPSPEED_KMH'], axis = 1)
df = df.drop(['BODYSTYLE'], axis = 1)
df = df.drop(['SEATS'], axis = 1)


df.columns



########################## 3.CREACION DE VARIABLES NUEVAS ###################################

''' Creamos la variable CAPACIDAD DE LA BATERIA como producto de la autonomia del coche y el 
    consumo del mismo. 
    
    Las unidades son: (km * Wh) / km --> Wh 
                      
    Wh/1000 --> kWH '''


df['BATTERY_CAPACITY'] = df['RANGE_KM'] * df['EFFICIENCY_WHKM'] / 1000



# Finalmente escribimos el dataframe en un csv
df.to_csv('electricCar_limpio.csv', index=False)

