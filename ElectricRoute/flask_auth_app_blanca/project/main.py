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
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from flask_mysqldb import MySQL
from .models import User, Ruta
from . import db


main = Blueprint('main', __name__)
# bp = Blueprint('errors', __name__)



# 2.- Páginas de error ----------------------------------------
#-----------------------------------------------------------------

@main.route('/page_not_found')
def page_not_found():
    return render_template('404.html')

# @bp.app_errorhandler(404)
# def handle_404(err):
#    return render_template('404.html'), 404


# 4.- Página index ------------------------------------------------
#------------------------------------------------------------------

@main.route('/index')
@login_required
def index():
    return render_template('index.html', name=current_user.name)


# 5.- Página ruta (mapa) ------------------------------------------
#------------------------------------------------------------------

@main.route('/Route')
@login_required
def route():
    return render_template('route.html', name=current_user.name)



@main.route('/Route', methods=['POST'])
@login_required
def route_post():
    
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', contacts = data)

    return render_template('route.html', name=current_user.name)





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




@main.route('/login_test')
def login_test():
    return render_template('login_test.html')
