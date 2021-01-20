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
        return redirect(url_for('main.index'))

    return render_template('login.html')




# 3- Página principal --------------------------------------------
#------------------------------------------------------------------

@main.route('/index')
def index():
    return render_template('index.html')



# 4.- Página prruta (mapa) ----------------------------------------
#------------------------------------------------------------------

@main.route('/Route')
def route():
    return render_template('ruta_2_puntos_v1.html')



# 5.- Página signup -----------------------------------------------
#------------------------------------------------------------------

@main.route('/profile')
def profile():
    return render_template('profile.html')



# 5.- Página logout -----------------------------------------------
#------------------------------------------------------------------

@main.route('/logout')
def logout():
    return 'Logout'


