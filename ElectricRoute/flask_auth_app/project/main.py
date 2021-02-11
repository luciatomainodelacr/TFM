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
from os import environ 


main = Blueprint('main', __name__)
bp = Blueprint('errors', __name__)


@main.before_request
def before_request():
   g.email = None
   if 'email' in session:
       g.email = session['email']



# 1.- Páginas de error ----------------------------------------
#-----------------------------------------------------------------

@main.app_errorhandler(404)
def handle_404(err):
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def handle_500(err):
    return render_template('500.html'), 500



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
        flash('Please log in!')
        return render_template('login.html')



# 3.- Página ruta (inicial) ---------------------------------------
#------------------------------------------------------------------

@main.route('/Route')
def route():

    # Se comprueba si la sesión del usuario está iniciada
    if g.email:

        # Se obtienen variables del usuario
        email   = session['email']
        name    = session['username']

        # Consulta a la bbdd
        cur = db.connection.cursor()
        cur.execute('''SELECT * FROM Ciudades''')
        ciudades_list = cur.fetchall()

        # Se inicializan dos listas para las ciudades y para las coordenadas
        lista_destino = []
        lista_coordenadas = []

        for ciudad in ciudades_list:
            lista_destino.append(ciudad[0])

        # Carga inicial y final
        rangeInitial = request.form.get('rangeInitial')
        rangeFinal   = request.form.get('rangeFinal')

        # Output página de ruta            
        return render_template('route.html', name = name, ciudades = lista_destino, lista_coordenadas=lista_coordenadas, rangeInitial=rangeInitial, rangeFinal=rangeFinal)

    # Si la sesión no está iniciada se le dirige a la página de inicio
    else:
        flash('Please log in!')
        return render_template('login.html')



# 4.- Página ruta (modelo) ----------------------------------------
#------------------------------------------------------------------

@main.route('/Route', methods=['GET', 'POST'])
def route_post():

    # Se comprueba si la sesión del usuario está iniciada
    if g.email:

        # Se obtienen variables del usuario
        email    = session['email']
        name     = session['username']
        brandCar = session['brandCar']
        modelCar = session['modelCar']

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

        # Carga inicial y final
        rangeInitial = request.form.get('rangeInitial')
        rangeFinal   = request.form.get('rangeFinal')

        # Tipo de programa
        programType = request.form.get('programType')


        # Se aplica el modelo para calcular la ruta
        ruta = main_route(tipo_programa = programType,
            marca_coche = brandCar,
            modelo_coche = modelCar,
            origen = ciudad_origen,
            destino = ciudad_destino,
            carga_inicial = rangeInitial,
            carga_final = rangeFinal,
            db_host = environ.get('DB_HOST')
        )
        
        # Lista de coordenadas de la ruta para dibujar en el mapa
        lista_coordenadas = []
        
        for i in range(0, len(ruta)):
            punto_coord = []
            latitud = ruta[i][0]
            longitud = ruta[i][1]
            punto_coord.append(latitud)
            punto_coord.append(longitud)
            lista_coordenadas.append(punto_coord)

        # Información sobre la ruta
        # ¡¡¡ FALTA MODIFICAR EL OUTPUT AÑADIR MÁS INFORMACIÓN EN UN DICCIONARIO!!!
        

        return render_template('route.html', name = name, ciudades = lista_destino, lista_coordenadas=lista_coordenadas, ciudad_origen=ciudad_origen, ciudad_destino=ciudad_destino, rangeInitial = rangeInitial, rangeFinal = rangeFinal, programType= programType)

    # Si la sesión no está iniciada se le dirige a la página de inicio
    else:
        flash('Please log in!')
        return render_template('login.html')
    
    

# 5.- Página Rutas Frecuentes -------------------------------------
#------------------------------------------------------------------

@main.route('/frequentroutes')
def frequentroutes():

    # Se comprueba si la sesión del usuario está iniciada
    if g.email:

        # Se obtienen variables del usuario
        email    = session['email']
        name     = session['username']

        # ¡! Añadir en la consulta el filtro usuario
        cur = db.connection.cursor()
        cur.execute('SELECT DISTINCT * FROM Output limit 5')
        rutas_list = cur.fetchall()

        dict_rutas = []
        list_rutas = ["From", "To", "Number of stops", "Time", "Load"]

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

@main.route('/profile', methods=['GET', 'POST'])
def profile():

    # Se comprueba si la sesión del usuario está iniciada
    if g.email:

        # Se obtienen variables del usuario
        email    = session['email']
        name     = session['username']
        lastName = session['lastName']
        brandCar = session['brandCar']
        modelCar = session['modelCar']

        return render_template('profile.html', email = email, name = name, lastName = lastName, brandCar = brandCar, modelCar = modelCar)

    # Si la sesión no está iniciada se le dirige a la página de inicio
    else:
        flash('Please log in!')
        return render_template('login.html')



# 7- Página profile edit ------------------------------------------
#------------------------------------------------------------------

@main.route('/profile', methods=['GET', 'POST'])
def profile_post():

    # Se comprueba si la sesión del usuario está iniciada
    if g.email:

        # Se obtienen variables del usuario
        email    = session['email']
        name     = session['username']
        lastName = session['lastName']
        brandCar = session['brandCar']
        modelCar = session['modelCar']

        if request.method == 'POST' and ('email' != '') and ('email' in request.form and 'username' in request.form and 'lastName' in request.form and 'mySelectBrand' in request.form and 'mySelectModel' in request.form):
            
            email    = request.form['email']
            username = request.form['username']
            lastName = request.form['lastName']
            brandCar = request.form.get('mySelectBrand')
            modelCar = request.form.get('mySelectModel')
        

        return render_template('profile.html', email = email, name = name, lastName = lastName, brandCar = brandCar, modelCar = modelCar)

    # Si la sesión no está iniciada se le dirige a la página de inicio
    else:
        flash('Please log in!')
        return render_template('login.html')



# 6- Página cars -----------------------------------------------
#------------------------------------------------------------------

@main.route('/cars', methods=['GET', 'POST'])
def cars():

    # Se comprueba si la sesión del usuario está iniciada
    if g.email:

        # Se obtienen variables del usuario
        email    = session['email']
        name     = session['username']
        lastName = session['lastName']
        brandCar = session['brandCar']
        modelCar = session['modelCar']

        # Consulta a la bbdd
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM ElectricCar WHERE BRAND = % s and MODEL = % s', (brandCar, modelCar, ))
        coches_list = cur.fetchall()

        # Variables
        rangeKm     = coches_list[0][2]
        efficiency  = coches_list[0][3]
        fastcharge  = coches_list[0][4]
        plugtype    = coches_list[0][6]
        battery     = coches_list[0][7]

        # Se inicializan dos listas para las ciudades y para las coordenadas
        lista_destino = []

        return render_template('cars.html', email = email, name = name, lastName = lastName,\
                                            brandCar = brandCar, modelCar = modelCar, rangeKm = rangeKm,\
                                            efficiency = efficiency, fastcharge = fastcharge,\
                                            plugtype = plugtype, battery = battery)

    # Si la sesión no está iniciada se le dirige a la página de inicio
    else:
        flash('Please log in!')
        return render_template('login.html')


# 8- Forgot Password ----------------------------------------------
#------------------------------------------------------------------

@main.route('/forgotpassword')
def forgotpassword():
    return render_template('forgotpassword.html')


# 9- Reset Password ----------------------------------------------
#------------------------------------------------------------------

@main.route('/resetpassword')
def resetpassword():
    return render_template('resetpassword.html')



# 8- Forgot Password ----------------------------------------------
#------------------------------------------------------------------

@main.route('/grafana_test')
def grafana_test():
    return render_template('grafana_test.html')