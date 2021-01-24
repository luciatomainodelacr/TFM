Esta carpeta contiene scripts y otro tipo de ficheros (.json para configuración por ejemplo) relacionados con el desarrollo de la aplicación.
A medida que se avance se pueden añadir distintas subcarpetas.

Se añaden tres carpetas correspondientes a cada uno de los módulos:
- Input: Contiene los scripts que obtienen los datos mediante csv y/o API, los filtran y analizan y luego los vuelcan a otros ficheros csv. 
  Contiene:
    - Gasolineras: carpeta con scripts referentes a los datos de Gasolineras_de_España.csv. 
      Los scripts son: 
      1) analizar_gasolineras.py -> Importar, limpiar, filtrar y reducir la dimensión (Clustering DBSCAN) de los datos de gasolineras.
    - PuntosRecarga: carpeta con scripts referentes a los datos de los puntos de recarga obtenidos con GoogleMapsAPI. 
      Los scripts son: 
      1) obtener_puntos_recarga_gmapi.py -> Descargar datos de Google Maps Places API para estaciones de recarga en las distintas CCAA.
      2) analizar_puntos_recarga.py -> Mergear los datos de CCAA en 1 solo y filtrar campos/registros innecesarios/erróneos;
                                       Eliminar duplicados y obtención a partir de la dirección la provincia y el código postal de cada punto de recarga;
                                       Reducir la dimensión (Clustering DBSCAN).

    - CochesElectricos: carpeta con scripts referentes a la limpieza de la BBDD de los coches eléctricos
      Los scripts son:
      1) limpieza_datos.py 
     - PuntosO_D: carpeta con scripts referentes a los puntos de origen y destino obtenidos a través de GoogleMapsAPI
       Los scripts son:
       1) API_Geocoding.py -> descarga de las coordenadas de las estaciones de tren y autobús de todas las capitales de provincia españolas mediante Geocoding API

- Modelo: Contiene los scripts que obtienen los datos mediante csv y/o API, los filtran y analizan y luego los vuelcan a otros ficheros csv. 
  Contiene:
    - Script matriz_distancias_api_google.py -> Importa el fichero de ciudades.csv y calcula mediande la API Google Distance Matrix las distancias entre todas las ciudades. Devuelve un archivo con cuatro columnas Origen, Destino, Distancia en metros, Distancia en km: ciudades_distancia.csv
    - Script calcular_caminos_entre_puntos.py -> Dadas dos ciudades origen-destino calcula la ruta optima entre ellas, o bien por el numero de nodos minimos necesarios para llegar o bien por el target que se le indique, en este caso, minimizar la distancia total.

    - _old:  carpeta que contiene script y dataset que se han utilizado como pruebas para construir procesos pero se han descartado por no ser óptimos.
    - Pruebas_Blanca: contiene script y dataset que se están utilizando para construir procesos pero todavía no están finalizados.
    - Modelo Avanzado: carpeta con scripts sobre la definición de la función objetivo y restricciones
      Los scripts son: 
      1) funcion_aux.py: conjuntos de funciones auxiliares
      2) main.py: prueba de uso de las funciones auxiliares de funcion_aux.py
- Output
