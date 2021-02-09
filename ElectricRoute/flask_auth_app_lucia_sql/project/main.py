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
from flask import Blueprint, render_template, redirect, url_for, request, flash, session, g
from flask_login import login_required, current_user
import datetime
from .BE.calcular_caminos_entre_puntos import main_route
from .BE.Output import BaseDatos
from . import db


main = Blueprint('main', __name__)
# bp = Blueprint('errors', __name__)


@main.before_request
def before_request():
   g.email = None
   if 'email' in session:
       g.email = session['email']



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
def index():

    # Se comprueba si la sesión del usuario está iniciada
    if g.email:
        email    = session['email']
        username = session['username']
        return render_template('index.html', name=username)

    # Si la sesión no está iniciada se le dirige a la página de inicio
    else:
        return render_template('login.html')



# 3.- Página ruta (inicial) ---------------------------------------
#------------------------------------------------------------------

@main.route('/Route')
def route():

    # Se obtienen variables del usuario
    email   = session['email']
    name    = session['username']

    # Se comprueba si la sesión del usuario está iniciada
    if g.email:

        # Consulta a la bbdd
        cur = db.connection.cursor()
        cur.execute('''SELECT * FROM Ciudades''')
        ciudades_list = cur.fetchall()

        # Se inicializan dos listas para las ciudades y para las coordenadas
        lista_destino = []
        lista_coordenadas = []

        for ciudad in ciudades_list:
            lista_destino.append(ciudad[0])

        # Output página de ruta            
        return render_template('route.html', name = name, ciudades = lista_destino, lista_coordenadas=lista_coordenadas)

    # Si la sesión no está iniciada se le dirige a la página de inicio
    else:
        return render_template('login.html')


# 3.- Página ruta (modelo) ----------------------------------------
#------------------------------------------------------------------

@main.route('/Route', methods=['GET', 'POST'])
def route_post():

    # Se obtienen variables del usuario
    email    = session['email']
    name     = session['username']
    brandCar = session['brandCar']
    modelCar = session['modelCar']

    # Se comprueba si la sesión del usuario está iniciada
    if g.email:

        # Consulta a la bbdd
        cur = db.connection.cursor()
        cur.execute('''SELECT * FROM Ciudades''')
        ciudades_list = cur.fetchall()

        # Se inicializan dos listas para las ciudades y para las coordenadas
        lista_destino = []

        for ciudad in ciudades_list:
            lista_destino.append(ciudad[0])
            
        ciudad_origen = request.form.get('mySelectOrigin')
        ciudad_destino = request.form.get('mySelectDest')

        ruta = main_route(tipo_programa = "ALL",
            marca_coche = brandCar,
            modelo_coche = modelCar,
            origen = ciudad_origen,
            destino = ciudad_destino
        )

        lista_coordenadas = []
        
        
        for i in range(0, len(ruta)):
            punto_coord = []
            latitud = ruta[i][0]
            longitud = ruta[i][1]
            punto_coord.append(latitud)
            punto_coord.append(longitud)
            lista_coordenadas.append(punto_coord)

        return render_template('route.html', name = name, ciudades = lista_destino, lista_coordenadas=lista_coordenadas )

    # Si la sesión no está iniciada se le dirige a la página de inicio
    else:
        return render_template('login.html')
    
    




# 4.- Página Rutas Frecuentes -------------------------------------
#------------------------------------------------------------------

@main.route('/frequentroutes')
def frequentroutes():

    email    = session['email']
    name     = session['username']

    # Se comprueba si la sesión del usuario está iniciada
    if g.email:

        # ¡! Añadir en la consulta el filtro usuario
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM Output limit 5')
        rutas_list = cur.fetchall()

        dict_rutas = []
        list_rutas = ["Origen", "Destino", "Número de Paradas", "Tiempo total", "Load"]

        for i in range(0, len(rutas_list)):
            
            dict_rutas.append({
                "Origen" : rutas_list[i][3],
                "Destino" : rutas_list[i][4],
                "Número de Paradas" : rutas_list[i][5],
                "Tiempo total" : rutas_list[i][7],
        })

        print(dict_rutas)

        return render_template('frequentroutes.html', email=email, list_rutas=list_rutas, dict_rutas=dict_rutas)
    
    # Si la sesión no está iniciada se le dirige a la página de inicio
    else:
        return render_template('login.html')
    

@main.route('/delete')
def delete():
    return render_template('delete.html', name=current_user.name)




# 6- Página profile -----------------------------------------------
#------------------------------------------------------------------

@main.route('/profile')
def profile():

    # Se obtienen variables del usuario
    email    = session['email']
    name     = session['username']
    lastName = session['lastName']
    brandCar = session['brandCar']
    modelCar = session['modelCar']

    # Se comprueba si la sesión del usuario está iniciada
    if g.email:
        return render_template('profile.html', email = email, name = name, lastName = lastName, brandCar = brandCar, modelCar = modelCar)

    # Si la sesión no está iniciada se le dirige a la página de inicio
    else:
        return render_template('login.html')



