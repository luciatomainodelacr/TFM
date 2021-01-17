En esta carpeta se guardaran los datasets que se van a utilizar, tanto es su formato original como tras haber sido limpiados y filtrados.
Se subdivide en cuatro carpetas, cada una con un tipo de dato:
- CochesElectricos: 
  Contiene:
    - coches electricos.zip: fichero comprimido con la información original
- Gasolineras:
  Contiene:
    - Gasolineras_de_España.csv: fichero original (sin acentos en el nombre de los campos)
    - gas_stations_categorical.txt: fichero txt con información de las variables categóricas del dataset (generado con script TFM/Python/Input/Gasolineras/analize_gas_stations.py)
    - gasolineras_filt_Espana.csv: fichero con dataset tras limpieza de variables y registros (generado con script TFM/Python/Input/Gasolineras/analize_gas_stations.py).
    - gasolineras_reduced_Espana.csv: fichero con dataset tras limpieza y reducción de dimensión con clustering DBSCAN (generado con script TFM/Python/Input/Gasolineras/analize_gas_stations.py) -> Este es el fichero que se tiene que utilizar para Gasolineras Propuestas con Puntos de Recarga (820 registros).
- PuntosRecarga:
  Contiene: 
    - GoogleMapsAPI: carpeta con ficheros csv con puntos de recarga obtenidos con Google Maps Places API (generado con script TFM/Python/Input/PuntosRecarga/get_ev_charging_stations_gmapi.py y TFM/Python/Input/PuntosRecarga/merge_ev_charging_stations.py) por CCAA y mergeados para toda España. 
    - OtrasFuentes: carpeta con ficheros csv con puntos de recarga de distintas CCAA (de momento no se usan).
    - puntos_carga_filt_Espana.csv: fichero con dataset tras limpieza y mergeo de los datos de GoogleMapsAPI por CCAA (generado con script TFM/Python/Input/PuntosRecarga/merge_ev_charging_stations.py). Se eliminan duplicados y se obtiene la provincia y el código postal para cada uno de los puntos de recarga.
- Ciudades
  Contiene:
    - ciudades.csv: fichero original con los puntos de cada una de las ciudades. Se corrige algunos detalles:
	* Ciudades mal geolocalizadas: Guadalajara, Córdoba, Alicante tren, Murcia tren. --> Se corrige
	* Ciudades dónde la estación de bus y tren tienen las mismas coordenadas: Almería, San Sebastián --> Se elimina uno de los puntos
    - ciudades_distancia.csv: matriz de distancias entre todas las ciudades. (Origen, Destino, Distancia en m)
