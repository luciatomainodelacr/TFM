# =============================================================================
#  Inicialización de la aplicación: __init__.py
# =============================================================================

"""
Este archivo tendrá la función de crear la aplicación, que iniciará la base de 
datos y registrará los molodelos.

Para ejecutar: 

1º) En un terminal de linux ir a la ruta:
>> cd Documentos/TFM/ElectricRoute/flask_auth_app

>> export FLASK_APP=project
>> export FLASK_DEBUG=1
>> flask run

2º) Abrir el navegador e ir a la ruta http://localhost:5000/login

3") Insertar un mail y una contraseña (cualquier)
Ejemplo: 
    User: blanca@hotmail.com
    Password: blanca

"""

# Se cargan las librerias
from flask import Flask
from flask_login import LoginManager
from flask_mysqldb import MySQL


# Se inicializa SQLAlchemy
#db = SQLAlchemy()

db = MySQL()


# Se crea la app
def create_app():
    
    app = Flask(__name__)

    app.config['MYSQL_HOST'] = 'localhost' 
    app.config['MYSQL_PORT'] = '3306'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'root'
    app.config['MYSQL_DB'] = 'tfm'

    app.secret_key = "123456789"


    db = MySQL(app)


    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


