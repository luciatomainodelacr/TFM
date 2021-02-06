# PYTHON

Esta carpeta contiene scripts y otro tipo de ficheros (.json para configuración por ejemplo) relacionados con el desarrollo de la aplicación.

El script principal, que contiene la función que se llamará desde el FE de Flask es: 

calcular_caminos_entre_puntos.py -> Este es el main al que tiene que llamar el FE, y que llama al resto de módulos de las distintas subcarpetas.
Dadas dos ciudades origen-destino calcula la ruta óptima entre ellas, o bien por el numero de nodos mínimos necesarios para llegar o bien por el target que se le indique, en este caso, minimizar la distancia total.
Para lanzar el script hay que pasarle 3 parámetros obligatorios:

1) ["PUNTO_RECARGA","GASOLINERA","ALL"]:Tipo de programa en base a los puntos que se quieren usar. Default: ALL

2) marca_coche: Marca de coche (tiene que estar en la tabla ElectricCar)

3) modelo_coche: Modelo de coche (tiene que estar en la tabla ElectricCar)

4) origen: Lugar de Origen (tiene que estar en la tabla Ciudades)

5) destino: Lugar de Origen (tiene que estar en la tabla Ciudades)

6) carga_inicial: Porcentaje de carga inicial del coche en lugar de origen. Default: 90

7) carga_final: Porcentaje de carga final del coche en lugar de destino. Default: 10
		
8) tipo_conector: Tipo de conector que necesita el coche (tiene que estar en la tabla PuntosCarga)

Se añaden tres carpetas correspondientes a cada uno de los módulos:

- __Input__

	Contiene los scripts que obtienen los datos mediante csv y/o API, los filtran y analizan y luego los vuelcan a otros ficheros csv. 

	- Gasolineras: carpeta con scripts referentes a los datos de Gasolineras_de_España.csv. 
	Los scripts son: 
	1) analizar_gasolineras.py -> Importar, limpiar, filtrar y reducir la dimensión (Clustering DBSCAN) de los datos de gasolineras.

	- PuntosRecarga: carpeta con scripts referentes a los datos de los puntos de recarga obtenidos con GoogleMapsAPI. 
	Los scripts son: 
	1) obtener_puntos_recarga_gmapi.py -> Descargar datos de Google Maps Places API para estaciones de recarga en las distintas CCAA.
	2) analizar_puntos_recarga.py -> Mergear los datos de CCAA en 1 solo y filtrar campos/registros innecesarios/erróneos;
									Eliminar duplicados y obtención a partir de la dirección la provincia y el código postal de cada punto de recarga;
									Reducir la dimensión (Clustering DBSCAN).
	3) puntos_carga_tomtomAPI.py -> Script que hace transacciones a la API de Tomtom para obtener la información relevante a los puntos de carga eléctrica (dirección, nº de conectores, tipo de conector, potencia)

	- CochesElectricos: carpeta con scripts referentes a la limpieza de la BBDD de los coches eléctricos
	Los scripts son:
	1) limpieza_datos.py 

	- PuntosO_D: carpeta con scripts referentes a los puntos de origen y destino obtenidos a través de GoogleMapsAPI
	Los scripts son:
	1) API_Geocoding.py -> descarga de las coordenadas de las estaciones de tren y autobús de todas las capitales de provincia españolas mediante Geocoding API

	- MatrizDistancias: carpeta con scripts referentes a las matrices de distancias entre ciudades, puntos de recarga y gasolineras.
	
	1) Script matriz_distancias_api_google.py -> Importa el fichero con todo el conjunto de puntos y calcula, mediande la API Google Distance Matrix, las distancias entre todas los puntos y el tiempo que se tarda en recorrer esa distancia. Devuelve un fichero con la información del Origen, Destino, Distancia y Duración del trayecto.

	2) Script matriz_distancias_Haversine.py -> Importa el fichero con todo el conjunto de puntos y calcula, mediande la distancia de Haversine, las distancias entre todas los puntos. Devuelve un fichero con la información del Origen, Destino y Distancia entre todas las combinaciones posibles.

- __Modelo__

	Contiene los scripts de los módulos del modelo de la aplicación.
	Los scripts son: 
	1) Network.py: funciones auxiliares basadas en el uso de la librería network
	2) Restricciones.py: funciones auxiliares para el cálculo de las restricciones 
	3) Tiempos.py: funciones auxiliares para el cálculo de los tiempos y otros (como la autonomía real de los coches)

	- Pruebas_Blanca: carpeta que contiene script y dataset que se estan utilizando para construir procesos pero todavía no estan finalizados.

- __Output__

	Contiene los scripts de los módulos del modelo de la aplicación.
	Los scripts son:
	1) BaseDatos.py: Clase que gestiona la conexión y las queries (tanto de input como de output) a la base de datos
