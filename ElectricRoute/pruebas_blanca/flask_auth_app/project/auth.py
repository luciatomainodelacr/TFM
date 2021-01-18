# =============================================================================
#  Modelo de autenticación: auth.py
# =============================================================================

"""
Dos páginas:
- login: página de inicio de sesión (/login)
- sign-up: página de registro (/sign-up)
- logout: ruta para cerrar la sesión de un usuario activo
"""

# Se cargan las librerias
from flask import Blueprint, render_template
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return 'Signup'

@auth.route('/logout')
def logout():
    return 'Logout'


