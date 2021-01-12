Esta carpeta contiene scripts y otro tipo de ficheros (.json para configuración por ejemplo) relacionados con el desarrollo de la aplicación.
A medida que se avance se pueden añadir distintas subcarpetas.

Se añaden tres carpetas correspondientes a cada uno de los módulos:
- Input: Contiene los scripts que obtienen los datos mediante csv y/o API, los filtran y analizan y luego los vuelcan a otros ficheros csv. 
  Contiene:
    - Gasolineras: carpeta con scripts referentes a los datos de Gasolineras_de_España.csv. 
      Los scripts son: 
      1) analize_gas_stations.py -> Importar, limpiar, filtrar y reducir la dimensión (Clustering DBSCAN) de los datos de gasolineras.
    - PuntosRecarga: carpeta con scripts referentes a los datos de los puntos de recarga obtenidos con GoogleMapsAPI. 
      Los scripts son: 
      1) get_ev_charging_stations_gmapi.py -> Descargar datos de Google Maps Places API para estaciones de recarga en las distintas CCAA.
      2) merge_ev_charging_stations.py -> Mergear los datos de CCAA en 1 solo y filtrar campos/registros innecesarios/erróneos.
    - CochesElectricos: carpeta con scripts referentes a la limpieza de la BBDD de los coches eléctricos
      Los scripts son:
      1) limpieza_datos.py 
     - PuntosO_D: carpeta con scripts referentes a los puntos de origen y destino obtenidos a través de GoogleMapsAPI
       Los scripts son:
       1) API_Geocoding.py -> descarga de las coordenadas de las estaciones de tren y autobús de todas las capitales de provincia españolas mediante Geocoding API
- Modelo
- Output
