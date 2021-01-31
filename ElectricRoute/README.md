# ELECTRICROUTE
Esta carpeta contiene la aplicación web desarrollada con Flask y otro tipo de ficheros que se han utilizado para realizar pruebas o desarrollos. (.html, .css, .py)

Se añaden dos carpetas:

- __ruta_con_indicaciones_v1__

	Contiene los html iniciales en los que se dibuja el mapa de españa y seleccionando dos puntos en el mapa te muestra la ruta por carretera con las indicaciones que se deben seguir. 

- __flask_auth_app__

	Contiene la aplicación web.

	* Para ejecutarla: 

		1º) En un terminal de linux ir a la ruta:
		>> cd Documentos/TFM/ElectricRoute/flask_auth_app

		>> export FLASK_APP=project
		>> export FLASK_DEBUG=1
		>> flask run

		2º) Abrir el navegador e ir a la ruta http://localhost:5000/login

		3º) Insertar un mail y una contraseña (cualquiera)
		Ejemplo: 
			User: blanca@hotmail.com
			Password: blanca
		Debería llevarnos a la pestaña Home

		4º) Navegar por el menú superior. (La mayoría de las vistas están en construcción)

	* Contiene:
	- script de python: __init__.py (crea la app que iniciará la base de datos y registrará los molodelos) y main.py (se construyen los modelos que llaman a los ficheros .html)
	- templates: contiene los ficheros .html. Se crean dos plantillas para el formato del resto de páginas: base.html y base_login.html
	- static: elementos estáticos como imágenes o ficheros .css para el estilo de los objetos.


- __flask_auth_app_blanca__

	  Carpeta que contiene una copia de la app en la que Blanca hace pruebas (en un futuro se borrará)
