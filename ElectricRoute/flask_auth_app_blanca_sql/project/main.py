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

from .Modelo.calcular_caminos_entre_puntos import main_route
from . import db


main = Blueprint('main', __name__)
# bp = Blueprint('errors', __name__)




# 1.- Páginas de error ----------------------------------------
#-----------------------------------------------------------------


@main.route('/ruta_test')
def ruta_test():

    ruta = main_route(tipo_programa = "ALL",
            marca_coche = "VOLKSWAGEN",
            modelo_coche = "ID3 PURE",
            origen = "Alicante Tren",
            destino = "A Corunia Bus"
    )

    return render_template('ruta_test.html', ruta=ruta)

