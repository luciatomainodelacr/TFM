# =============================================================================
#  Inicialización de la aplicación: __init__.py
# =============================================================================

"""
Este archivo tendrá la función de crear la aplicación, que iniciará la base de 
datos y registrará los molodelos.

Para ejecutar: 

1º) En un terminal de linux ir a la ruta:
>> cd Documentos/TFM/ElectricRoute/flask_auth_app_blanca

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
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


# Se inicializa SQLAlchemy (se utilizará más adelante)
db = SQLAlchemy()

# Se crea la app
def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

