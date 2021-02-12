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
from flask_mysqldb import MySQL
import MySQLdb.cursors 
import mysql.connector
from os import environ 
from .BE.calcular_caminos_entre_puntos import main_route
from .BE.Output import BaseDatos
from . import db


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
        user_id  = session['id']
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
            user_id = user_id,
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
        #  Consulta a la bbdd para obtener el scenario
        curScenario = db.connection.cursor(MySQLdb.cursors.DictCursor)
        curScenario.execute("""SELECT scenario_id FROM Output ORDER BY scenario_id DESC LIMIT 1""")
        dict_scenario_id = curScenario.fetchall()
        
        scenario_id = dict_scenario_id[0]["scenario_id"]

        #  Consulta a la bbdd
        curDetalleRuta = db.connection.cursor(MySQLdb.cursors.DictCursor)
        curDetalleRuta.execute("SELECT * FROM Output WHERE scenario_id LIKE % s ", [scenario_id])
        rutas_info = curDetalleRuta.fetchall()

        rutas_info_aux = rutas_info[0]["path"]

        lista_Puntos_aux = rutas_info_aux.split('-')


        # ¡¡¡ FALTA MODIFICAR EL OUTPUT AÑADIR MÁS INFORMACIÓN EN UN DICCIONARIO!!!
        

        return render_template('route.html', name = name, ciudades = lista_destino, lista_coordenadas=lista_coordenadas, ciudad_origen=ciudad_origen, ciudad_destino=ciudad_destino, rangeInitial = rangeInitial, rangeFinal = rangeFinal, programType= programType, lista_Puntos_aux=lista_Puntos_aux)

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
        user_id  = session['id']
        email    = session['email']
        name     = session['username']

        #  Consulta a la bbdd
        sql_query = "SELECT DISTINCT * FROM Output WHERE user_id = % s limit 5"
        argumentos = str(user_id)
        
        curFrequent = db.connection.cursor(MySQLdb.cursors.DictCursor)
        curFrequent.execute(sql_query, argumentos)
        rutas_list = curFrequent.fetchall()


        dict_rutas = []
        list_rutas = ["From", "To", "Number of stops", "Time"]

        if (len(rutas_list) == 1):
            dict_rutas.append({
                "Origen"            : rutas_list[0]["origen"],
                "Destino"           : rutas_list[0]["destino"],
                "Número de Paradas" : rutas_list[0]["num_paradas"],
                "Tiempo total"      : rutas_list[0]["tiempo_total"]
            })
        
        else:
            
            for i in range(0, len(rutas_list)):
                dict_rutas.append({
                    "Origen"            : rutas_list[i]["origen"],
                    "Destino"           : rutas_list[i]["destino"],
                    "Número de Paradas" : rutas_list[i]["num_paradas"],
                    "Tiempo total"      : rutas_list[i]["tiempo_total"]
                })

        return render_template('frequentroutes.html', email=email, list_rutas=list_rutas, dict_rutas=dict_rutas)
    
    # Si la sesión no está iniciada se le dirige a la página de inicio
    else:
        return render_template('login.html')
    




# 6- Página profile -----------------------------------------------
#------------------------------------------------------------------

@main.route('/profile')
def profile():

    # Se comprueba si la sesión del usuario está iniciada
    if g.email:

        # Se obtienen variables del usuario
        email    = session['email']
        name     = session['username']
        lastName = session['lastName']
        brandCar = session['brandCar']
        modelCar = session['modelCar']

        # Consulta a la bbdd ElectricCar
        cur = db.connection.cursor()
        cur.execute('''SELECT * FROM ElectricCar''')
        electricCar_list = cur.fetchall()

        # Se inicializan dos listas para las marcas y los modelos de coche
        list_brand = []
        list_model = []

        for coche in electricCar_list:
            list_brand.append(coche[0])
            list_model.append(coche[1])

        return render_template('profile.html', email = email, name = name, lastName = lastName, brandCar = brandCar, modelCar = modelCar, list_brand = list_brand, list_model = list_model)

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
        id       = session['id']
        email    = session['email']
        name     = session['username']
        lastName = session['lastName']
        brandCar = session['brandCar']
        modelCar = session['modelCar']

        # Consulta a la bbdd ElectricCar
        cur = db.connection.cursor()
        cur.execute('''SELECT * FROM ElectricCar''')
        electricCar_list = cur.fetchall()

        # Se inicializan dos listas para las marcas y los modelos de coche
        list_brand = []
        list_model = []

        for coche in electricCar_list:
            list_brand.append(coche[0])
            list_model.append(coche[1])


        if request.method == 'POST' and ('email' != '') and ('usernameEdit' in request.form and 'lastNameEdit' in request.form and 'mySelectBrandEdit' in request.form and 'mySelectModelEdit' in request.form):
            
            id       = session['id']

            if (request.form['emailEdit'] != ''):
                email              = request.form['emailEdit']
                session['email']   = request.form['emailEdit']
            
            if (request.form['usernameEdit'] != ''):
                name                = request.form['usernameEdit']
                session['username'] = request.form['usernameEdit']
            
            if (request.form['lastNameEdit'] != ''):
                lastName            = request.form['lastNameEdit']
                session['lastName'] = request.form['lastNameEdit']

            if (request.form['mySelectBrandEdit'] != ''):
                brandCar            = request.form['mySelectBrandEdit']
                session['brandCar'] = request.form['mySelectBrandEdit']
           
            if (request.form['mySelectModelEdit'] != ''):
                modelCar            = request.form['mySelectModelEdit']
                session['modelCar'] = request.form['mySelectModelEdit']

            
            # Consulta a la bbdd users 
            sql_query = "UPDATE users SET username = %s, lastName = %s, brandCar = %s, modelCar = %s  WHERE id = %s AND email = %s"
            argumentos = (name, lastName, brandCar, modelCar, id, email)

            curProfile = db.connection.cursor(MySQLdb.cursors.DictCursor)
            curProfile.execute(sql_query, argumentos)
            db.connection.commit() 
        


        return render_template('profile.html', email = email, name = name, lastName = lastName, brandCar = brandCar, modelCar = modelCar, list_brand = list_brand, list_model = list_model)

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