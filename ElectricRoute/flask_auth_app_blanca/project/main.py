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
from flask_login import login_required, current_user
from . import db


main = Blueprint('main', __name__)


# 2.- Páginas de error ----------------------------------------
#-----------------------------------------------------------------


# 4.- Página index ------------------------------------------------
#------------------------------------------------------------------

@main.route('/index', methods = ["GET", "POST"])
@login_required
def index():
    return render_template('index.html', name=current_user.name)



# 5.- Página ruta (mapa) ------------------------------------------
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




