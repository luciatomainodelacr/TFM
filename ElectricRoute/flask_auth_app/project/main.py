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
from .models import User, Route, ciudades, ElectricCar
from . import db


main = Blueprint('main', __name__)
# bp = Blueprint('errors', __name__)



# 1.- Páginas de error ----------------------------------------
#-----------------------------------------------------------------

@main.route('/page_not_found')
def page_not_found():
    return render_template('404.html')

# @bp.app_errorhandler(404)
# def handle_404(err):
#    return render_template('404.html'), 404



# 2.- Página index ------------------------------------------------
#------------------------------------------------------------------

@main.route('/index')
@login_required
def index():
    return render_template('index.html', name=current_user.name)



# 3.- Página ruta (mapa) ------------------------------------------
#------------------------------------------------------------------

@main.route('/Route')
@login_required
def route():

    ciudades_list = ciudades.query.all()
    lista_destino = []

    for ciudad in ciudades_list:
        lista_destino.append(ciudad.id)

    return render_template('route.html', name = current_user.name, ciudades = lista_destino)



@main.route('/Route', methods=['POST'])
@login_required
def route_post():

    ciudades_list = ciudades.query.all()
    ciudades_dict = {}

    for ciudad in ciudades_dict:

        ciudades_dict = {

            "provincia"   : ciudad.provincia,
            "Direccion"   : ciudad.Direccion,
            "Latitud"     : ciudad.Latitud,
            "Longitud"    : ciudad.Longitud,
            "Coordenadas" : ciudad.Coordenadas
        }       

    return render_template('route.html', name=current_user.name, ciudades_dict = ciudades_dict)



# 4.- Página Rutas Frecuentes -------------------------------------
#------------------------------------------------------------------

@main.route('/frequentroutes')
@login_required
def frequentroutes():
    rutas_list = Route.query.filter_by(email=current_user.email).order_by("dateSearch")[::-1] 
    dict_rutas= {}

    for ruta in rutas_list:
        
        dict_rutas = {
            "From" : ruta.from_ub,
            "To" : ruta.to_ub,
            "Type Car" : ruta.typeCar,
            "Load of the car" : ruta.typeLoad
        }   

    return render_template('frequentroutes.html', email=current_user.email, dict_rutas=dict_rutas)



# 5.- Página profile -----------------------------------------------
#------------------------------------------------------------------

@main.route('/profile2')
@login_required
def profile2():
    return render_template('profile2.html', email=current_user.email, name=current_user.name, lastName=current_user.lastName, typeCar=current_user.typeCar)



