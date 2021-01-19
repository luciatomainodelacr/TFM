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
from flask import Blueprint, Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from . import db

auth = Blueprint('auth', __name__)

# Página para logearse
@auth.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        next = request.args.get('next', None)
        if next:
            return redirect(next)
        return redirect(url_for('main.index'))
    return render_template('login.html')



# Página para registrarse
@auth.route('/signup')
def signup():
    return 'Signup'


# Pagína logout
@auth.route('/logout')
def logout():
    return 'Logout'


