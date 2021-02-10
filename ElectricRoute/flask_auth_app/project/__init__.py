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
>> Si se va a lanzar flask_app en local: export DB_HOST=0.0.0.0
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
from os import environ 
from .BE.Output import BaseDatos



# Se inicializa SQLAlchemy
db = MySQL()

# Se crea la app
def create_app():
    app = Flask(__name__)

    db_host = environ.get('DB_HOST')
    app.config['MYSQL_HOST'] = db_host
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'root'
    app.config['MYSQL_DB'] = 'tfm'                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
    app.config['MYSQL_DATABASE_PORT'] = '3306'

    app.secret_key = "123456789"

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        #return User.query.get(int(user_id))
        return 1


    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


