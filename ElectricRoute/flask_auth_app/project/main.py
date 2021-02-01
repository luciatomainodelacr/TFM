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
from flask import Blueprint, render_template
from flask_login import login_required, current_user



main = Blueprint('main', __name__)


# 3.- Página forgot-password --------------------------------------
#------------------------------------------------------------------

@main.route('/password', methods = ["GET", "POST"])
def password():
    return render_template('password.html')



@main.route('/password1', methods = ["GET", "POST"])
def password1():
    return render_template('password1.html')


# 4.- Página index ------------------------------------------------
#------------------------------------------------------------------

@main.route('/index')
@login_required
def index():
    return render_template('index.html', name=current_user.name)


# 5.- Página ruta (mapa) ------------------------------------------
#------------------------------------------------------------------

@main.route('/Route', methods = ["GET", "POST"])
@login_required
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




