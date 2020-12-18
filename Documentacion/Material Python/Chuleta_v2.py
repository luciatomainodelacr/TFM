
"""
Autor: Blanca Alonso

Chuleta y ayudas para comandos en Python

"""

# =============================================================================
# 0.- ESTABLECER DIRECTORIO
# =============================================================================

import os
os.chdir("path")

# ¡IMPORTANTE! Las barras del directorio deben ser dobles \\



# =============================================================================
# 1.- CARGA DE PAQUETES
# =============================================================================

# Librerías numpy: biblioteca de álgebra lineal más conocida

import numpy as np


# Librería pandas: tratamiento de datos estructurados, semi y no estructurados
import pandas as pd 



# =============================================================================
# 2.- LECTURA Y ESCRITURA 
# =============================================================================

# CSV
df = pd.read_csv("Input.csv", sep = ";", decimal = ",")  # lectura
df.to_csv("Output.csv", sep = ";", index = False) # escritura


# EXCEL
df = pd.read_excel("Input.xlsx")
df.to_excel("Output.xlsx", index = False)



# =============================================================================
# 3.- TRATAMNIENTO BBDD
# =============================================================================

# Limpiar datos
df['campo'].str.replace(r" \(.*\)","")

# Tipos de datos de cada columna del dataframe
df.dtypes

# Cambiar el tipo de dato
df['campo'].astype(str)

# Nombres de tablas a mayusculas (dos formas distintas)
df.columns = df.columns.str.upper()
df.columns = map(lambda x: str(x).upper(), df.columns)
  

# Convertir todos los valores de un campo a mayúsculas
df['campo'] = df['campo'].str.upper()


# Lista con x nombres de las columnas definido con un rango
colnames_df = list(df.columns[2:4])


# Cambiar los nombres de todos los campos de la tabla segun el orden en el que están
df.columns = ['campo_nuevo1', 'campo_nuevo2', 'campo_nuevo3']
df = df.rename(columns = {"campo_now1": "campo_new1", "campo_now2": "campo_new2"})


# Quitar espacios en blanco en los nombres de las columnas o en un campo
df.columns = df.columns.str.strip()                             # trim 
df.columns = df.columns.str.strip().str.replace(' ', '')        # replace
df['campo'] = df.campo.str.strip().str.replace(' ', 'vacío') 
df['campo'] = df.campo.str.strip().replace('...', 'vacío')

# Reemplazar valores según sea igual o no a un valor
df['campo'] = np.where(df.TOTAL_PAQUETE.isin(['condicion1', 'condicion2']),
              df['campo'] , 'Otros')


# Select
df.columna  # Una columna
df = df[["columna1", "columna2", "columna3"]]   # Varias columnas

# Seleccionar x columnas según un filtro
df.loc[df['columna1' > 10], ['columna1', 'columna2']]


# Eliminar una columna
df = df.drop(columns = 'Columna') 
df = df.drop(['Columna'], axis = 1)
 
 
# NaN
df.isnull()                     # Para comprobar si hay NaN
df.notnull()                     # Para comprobar si no hay NaN
df.dropna()                     # Elimina cualquier fila con NaN    
df.fillna(value = 0)            # Reemplaza los NaN por un valor
df = df[df['campo'].notna()]    # Elimina los NaN de una columna 

list(df['campo'].isnull()).count(True) # Comprobar NA's en una columna

# Imputation Na
from sklearn.impute import SimpleImputer
my_imputer = SimpleImputer(strategy = 'XX') #a que se quieren imputar: median, constant (númerico), most_frequent
imputed_X_train = pd.DataFrame(my_imputer.fit_transform(X_train))

# Quitar duplicados
df = df.drop_duplicates()


# Valores distintos de una columna
df['columna'].nunique() # devuelve un int de cuántos valores != hay
df['columna'].unique()  # devuelve un array con los != valores


# Apendizar dos dataframes por filas
df1 = df1.append(df2) 
df = pd.concat([df1, df2])


# Apendizar dos dataframes por filas
df = pd.concat([df1, df2])

# Calcular el máximo según un campo
df[df['CAMPO'] == 'FILTRO'].CAMPO_NUMERICO.max()

# Recuento de la frecuencia de los valores de una columna
df['CAMPO'].value_counts()


# Dividir una columna en dos por un delimitador
df[['CAMPO1','CAMPO2']] = df['CAMPO1'].str.split(',',expand=True)

# Borrar NA´s
df.dropna(axis=0)

# Ordenar
DF.sort_values (by )
DF.sort_index()


# 3.1.- FECHAS
# --------------------------------------------------------------------------#

import datetime as dt

# Transformar un campo a fecha
df['FECHA'] = pd.to_datetime(df['FECHA'])

# Extraer el año, mes, día
df['ANIO'] = df['FECHA'].dt.year



# =============================================================================
# 4.-  OPERACIONES CON LAS BBDD
# =============================================================================

# Resumen de los datos con la media, desviación tipica, cuartiles
DF.describe()

# Primeras filas
DF.head()

# Aparecen las columnas
DF.columns

# Cuenta las veces que aparece un elemento en una lista
lista.count(valor)

# En un dataframe
list(df['CAMPO']).count('valor')


# Crear columnas condicionales
obs_pres_med = [x for x in obs if "Prescripción Médica" in x]

df['Prescr_Medica'] = df.Observaciones.apply(lambda x: 'SI' if x in obs_pres_med else 'NO')



# Transformar un dataframe a diccionario
df_dict = df.set_index('key').T.to_dict('list')



# =============================================================================
# 5.- CRUCES
# =============================================================================

# ¡OJO! Asegurarse que df2 no tenga duplicados en la clave

# Inner Join: valores coincidentes
df1.merge(df2, how = "inner", on = "CLAVE")

# Left y right join
df1.merge(df2, how = "left", on = "CLAVE")
df1.merge(df2, how = "right", on = "CLAVE")

# Full join: unimos las dos tablas crucen o no
df1.merge(df2, how = "outer", on = "CLAVE")

# Si los campos no tienen el mismo nombre
df1.merge(df2, how = "left", left_on = "CLAVE_df_uno", right_on = "CLAVE_df2")


# Si queremos seleccionar sólo algunos campos del dataframe 2
df1.merge(df2[["campos"]], how = "left", left_on = "CLAVE_df_uno",
          right_on = "CLAVE_df2")

# Cruzar por varios campos 
df1.merge(df2, how = "left", on = ["CAMPO1", "CAMPO2"])



# =============================================================================
# 6.- BUCLES FOR & IF
# =============================================================================

# Para obtener los diferentes valores de error si se cambian parametros en cada modelo

from sklearn.metrics import mean_absolute_error
from sklearn.tree import DecisionTreeRegressor

def get_mae(max_leaf_nodes, train_X, val_X, train_y, val_y):
    model = DecisionTreeRegressor(max_leaf_nodes=max_leaf_nodes, random_state=0)
    model.fit(train_X, train_y)
    preds_val = model.predict(val_X)
    mae = mean_absolute_error(val_y, preds_val)
    return(mae)
    
 for max_leaf_nodes in [5, 50, 500, 5000]:
    my_mae = get_mae(max_leaf_nodes, train_X, val_X, train_y, val_y)
    print("Max leaf nodes: %d  \t\t Mean Absolute Error:  %d" %(max_leaf_nodes, my_mae))



# =============================================================================
# 7.- TOTALIZACIONES
# =============================================================================

# Totalizar
df = df.groupby("CAMPO").sum()                  # Por una variable
df = df.groupby(["CAMPO1", "CAMPO2"]).sum()     # Por varias variables

# Totalizar realizando distintas operaciones segun el campo
df = df.groupby("CAMPO").agg({'CAMPO_num1': sum, 'CAMPO_num2' : max}) 

# Totalizar definiendo un campo nuevo en base a otro
df = df.set_index('CAMPO').groupby(level = 0)['CAMPO_num1'].agg({'CAMPO_new' : np.sum})



# =============================================================================
# 8.- FUNCIONES LAMBDA
# =============================================================================









# =============================================================================
# 9.- MACHINE LEARNING
# =============================================================================

# Definir una semilla
import random
random.seed(1234)

# Dividimos en train y test
from sklearn.model_selection import train_test_split

datos_spliteados = train_test_split(df,
                                    train_size = 0.8,     # 80% training
                                    test_size = 0.2       # 20% testing
                                   )

df_training_set = datos_spliteados[0]
df_test_set = datos_spliteados[1]


# 9.1.- Regresión Logístico ----------------------------------------------
# --------------------------------------------------------------------------#

from sklearn.linear_model import LogisticRegression

# Creamos una instancia del modelo, con todos los hiperparámetros y argumentos 
# por defecto:

lr = LogisticRegression()

# Ahora vamos a entrenarla con el conjunto de training:
lr.fit(X = dataset_clasificacion_training[["hormona_a", "hormona_b"]], # features
       y = dataset_clasificacion_training["label"])                    # labels
       
       

# 9.2.- Arboles----------------------------------------------
# --------------------------------------------------------------------------#
from sklearn.tree import DecisionTreeRegressor

# Define model. Specify a number for random_state to ensure same results each run
TR_model = DecisionTreeRegressor(random_state=1) # = 1 para que siempre se cree el mismo modelo

# Ahora vamos a entrenarla con el conjunto de training:
DF.fit(X_train, y_train)

# 9.3.- Random Forest----------------------------------------------
# --------------------------------------------------------------------------#
from sklearn.ensemble import RandomForestRegressor

# Define model. Specify a number for random_state to ensure same results each run
forest_model = RandomForestRegressor(random_state=1) # = 1 para que siempre se cree el mismo modelo

# Ahora vamos a entrenarla con el conjunto de training:
DF.fit(X_train, y_train)


# 9.4.- XGBoost---------------------------------------------
# --------------------------------------------------------------------------#
from xgboost import XGBRegressor

my_model = XGBRegressor(n_estimators=1000, learning_rate=0.05)
my_model.fit(X_train, y_train,  early_stopping_rounds=5, 
             eval_set=[(X_valid, y_valid)], 
             verbose=False)
             
# 9.5.- Cross Validation---------------------------------------------
# --------------------------------------------------------------------------#
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

my_pipeline = Pipeline(steps=[('preprocessor', SimpleImputer()), # imputar los missings a lo que se decida
                              ('model', RandomForestRegressor(n_estimators=50,
                                                              random_state=0))
                             ])
                             

from sklearn.model_selection import cross_val_score

# Multiply by -1 since sklearn calculates *negative* MAE
scores = -1 * cross_val_score(my_pipeline, X, y,
                              cv=5,
                              scoring='neg_mean_absolute_error')

print("MAE scores:\n", scores) 

# 9.6.- Predicción y error----------------------------------------------
# --------------------------------------------------------------------------#
from sklearn.metrics import mean_absolute_error

prediccion = Df.predict(X)
mean_absolute_error(y, prediccion)

# 9.7.- Output---------------------------------------------
# --------------------------------------------------------------------------#
output = pd.DataFrame({'Id': X_test.index,
                       'Target': preds_test})
output.to_csv('nombre_archivo.csv', index=False)




# =============================================================================
# 10.- OTRAS COSAS
# =============================================================================

from  pandas.io.json  import  json_normalize

# Normalizar los datos 
df  =  json_normalize(creds)









