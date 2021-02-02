# DATASETS

En esta carpeta se guardaran los datasets que se van a utilizar, tanto es su formato original como tras haber sido limpiados y filtrados.
Se subdivide en cuatro carpetas, cada una con un tipo de dato:

- __CochesElectricos__

	Contiene:
	- coches electricos.zip: fichero comprimido con la información original
	- Creacion_nuevas_variables: fichero txt donde aparecerán (posibles)variables nuevas interesantes para nuestro objetivo
	- Datos_usuario: fichero txt donde se establecen los datos solicitados al usuario de la aplicación
	- Info_var_coches: fichero txt que contiene una lista de páginas web con información útil acerca de las variables input y de los coches eléctricos en general
	- Pasos_limpieza_coches: fichero txt que contiene una breve descripción de cada variable input de la BBDD de los coches, así como los pasos seguidos para su limpieza

- __Gasolineras__

	Contiene:
	- Gasolineras_de_España.csv: fichero original (sin acentos en el nombre de los campos)
	- gas_stations_categorical.txt: fichero txt con información de las variables categóricas del dataset (generado con script TFM/Python/Input/Gasolineras/analizar_gasolineras.py)
	- gasolineras_filt_Espana.csv: fichero con dataset tras limpieza de variables y registros (generado con script TFM/Python/Input/Gasolineras/analizar_gasolineras.py).
	- gasolineras_reduced_Espana.csv: fichero con dataset tras limpieza y reducción de dimensión con clustering DBSCAN (generado con script TFM/Python/Input/Gasolineras/analizar_gasolineras.py) -> Este es el fichero que se tiene que utilizar para Gasolineras Propuestas con Puntos de Recarga (341 registros).

- __MatrizDistancias__

	Contiene:
	- matriz_distancia_haversine.csv: matriz de distancias entre todo el conjunto de puntos considerados (ciudades, puntos de regarla y gasolineras), se calcula utilizando la distancia de Haversine.  -> Este es el fichero que se tiene que utilizar como matriz de distancias (598.303 registros)
	- pruebas_google_api: carpeta que contiene distintos dataset obtenidos con la API de Google, Distance Matrix [Pruebas Blanca, se borrará a futuro]
		* ciudades_distancia.csv: matriz de distancias entre todas las ciudades. (Origen, Destino, Distancia en m)
		* matriz_distancias_input.csv: fichero con la información input (id, provincia, lat, long) de todo el conjunto de puntos.
		* matriz_distancia_v1.csv: fichero que contiene el primer output de la API de Google, contiene la distancia y el tiempo de las 23 primeras ciudades con todo el conjunto.
		* matriz_distancia_v2.csv: fichero que contiene el segundo output de la API de Google, contiene la distancia y el tiempo de las 33 siguientes ciudades con todo el conjunto.
		* puntos_kk: fichero que contiene aquellos puntos filtrados que se van a utilizar para hacer las llamadas a la API. Es necesario dividir el dataframe original para evitar lanzar muchas llamadas y que el coste sea elevado.
	
- __PuntosO_D__

	Contiene:
	- GeocodingAPI: carpeta con el fichero csv de los puntos de origen y destino (expresados en coordenadas geográficas). Se trata de las coordendas de las estaciones de tren y autobús de todas las capitales de provincia españolas.
	  Contiene ciudades.csv: fichero original con los puntos de cada una de las ciudades. Se corrige algunos detalles:
		* Ciudades mal geolocalizadas: Guadalajara, Córdoba, Alicante tren, Murcia tren. --> Se corrige
		* Ciudades dónde la estación de bus y tren tienen las mismas coordenadas: Almería, San Sebastián --> Se elimina uno de los puntos
	
	
- __PuntosRecarga__

	Contiene: 
	- GoogleMapsAPI: carpeta con ficheros csv con puntos de recarga obtenidos con Google Maps Places API (generado con script TFM/Python/Input/PuntosRecarga/obtener_puntos_recarga_gmapi.py y TFM/Python/Input/PuntosRecarga/analizar_puntos_recarga.py) por CCAA y mergeados para toda España. 
	- puntos_carga_filt_Espana.csv: fichero con dataset tras limpieza y mergeo de los datos de GoogleMapsAPI por CCAA (generado con script TFM/Python/Input/PuntosRecarga/analizar_puntos_recarga.py). Se eliminan duplicados y se obtiene la provincia y el código postal para cada uno de los puntos de recarga.
	- puntos_carga_reduced_Espana.csv: fichero con dataset tras limpieza y reducción de dimensión con clustering DBSCAN por CCAA (generado con script TFM/Python/Input/PuntosRecarga/analizar_puntos_recarga.py)
	- ptos_recarga_info.csv: fichero con dataset tras obtener toda la información acerca de los puntos de recarga: nº de conectores, tipo de conector y potencia. (generado con script TFM/Python/Input/PuntosRecarga/puntos_carga_tomtomAPI.py) -> Este es el fichero definitivo que se tiene que utilizar para Puntos de Recarga (353 registros).
