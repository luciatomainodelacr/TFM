# =============================================================================
#  Modelo principal: main.py
# =============================================================================

"""
Dos páginas:
- index: página principal (/)
- profile: página de perfil para cuando se inicie sesión (/Profile)

Modelo de autenticación. Tres páginas:
- login: página de inicio de sesión (/login)
- sign-up: página de registro (/sign-up)
- logout: ruta para cerrar la sesión de un usuario activo

"""


# Se cargan las librerias
from flask import Blueprint, Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from . import db



main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)




# 2.- Página para logearse ----------------------------------------
#------------------------------------------------------------------

@main.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        next = request.args.get('next', None)
        if next:
            return redirect(url_for('next'))
        return redirect(url_for('index'))

    return render_template('login.html')


# 3.- Página register ---------------------------------------------
#------------------------------------------------------------------

@main.route('/register', methods = ["GET", "POST"])
def register():
    return render_template('register.html')


# 4.- Página index ------------------------------------------------
#------------------------------------------------------------------

@main.route('/index', methods = ["GET", "POST"])
def index():
    return render_template('index.html')



# 5.- Página ruta (mapa) ----------------------------------------
#------------------------------------------------------------------

@main.route('/Route', methods = ["GET", "POST"])
def route():
    return render_template('route.html')


# 6.- Página Rutas Frecuentes -------------------------------------
#------------------------------------------------------------------

@main.route('/rutasFrecuentes')
def rutasFrecuentes():
    return 'Rutas Frecuentes'



# 7.- Página profile -----------------------------------------------
#------------------------------------------------------------------

@main.route('/profile', methods = ['POST', 'GET'])
def profile():
    return render_template('profile.html')


# 8.- Password-----------------------------------------------
#------------------------------------------------------------------
@main.route('/password1', methods = ['POST', 'GET'])
def password1():
    return render_template('password1.html')

# 9.- Settings-----------------------------------------------
#------------------------------------------------------------------
@main.route('/Settings', methods = ['POST', 'GET'])
def Settings():
    return render_template('Settings.html')