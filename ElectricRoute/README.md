# ELECTRICROUTE
Esta carpeta contiene la aplicación web desarrollada con Flask y otro tipo de ficheros que se han utilizado para realizar pruebas o desarrollos. (.html, .css, .py)

Se añaden dos carpetas:

- __flask_auth_app__

	Contiene la aplicación web.

	* Para ejecutarla: 

		1º) En un terminal de linux ir a la ruta:
		>> cd Documentos/TFM/ElectricRoute/flask_auth_app

		>> export FLASK_APP=project
		>> export FLASK_DEBUG=1
		>> export DB_HOST=0.0.0.0
		>> export GRAFANA_HOST=0.0.0.0
		
		>> flask run

		2º) Abrir el navegador e ir a la ruta http://localhost:5000/login

		3º) Si se tiene un usuario, logearse. En otro caso, crear una nueva cuenta "Create an Account!"


	* Contiene:
	- script de python: __init__.py (crea la app que iniciará la base de datos y registrará los molodelos), auth.py y main.py (se construyen los modelos que llaman a los ficheros .html)
	- templates: contiene los ficheros .html. Se crean dos plantillas para el formato del resto de páginas: base.html y base_login.html
	- static: elementos estáticos como imágenes o ficheros .css para el estilo de los objetos.
