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
#from .models import User, Route, ciudades, ElectricCar
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
    if g.email:
        email = session['email']
        return render_template('index.html', name=email)
    else:
        return render_template('login.html')



# 3.- Página ruta (mapa) ------------------------------------------
#------------------------------------------------------------------

@main.route('/Route')
def route():

    email    = session['email']
    name    = session['username']

    if g.email:
    
        cur = db.connection.cursor()
        cur.execute('''SELECT * FROM Ciudades''')
        ciudades_list = cur.fetchall()
        lista_destino = []

        for ciudad in ciudades_list:
            lista_destino.append(ciudad[0])
            
        return render_template('route.html', name = name, ciudades = lista_destino)

    else:
        return render_template('login.html')



@main.route('/Route', methods=['GET', 'POST'])
def route_post():

    email    = session['email']
    name     = session['username']
    brandCar = session['brandCar']
    modelCar = session['modelCar']

    if g.email:

        cur = db.connection.cursor()
        cur.execute('''SELECT * FROM Ciudades''')
        ciudades_list = cur.fetchall()
        lista_destino = []

        for ciudad in ciudades_list:
            lista_destino.append(ciudad[0])
            
        ciudad_origen = request.form.get('mySelectOrigin')
        ciudad_destino = request.form.get('mySelectDest')

       

        return render_template('route.html', name = name, ciudades = lista_destino)

    else:
        return render_template('login.html')
    






# 4.- Página Rutas Frecuentes -------------------------------------
#------------------------------------------------------------------

@main.route('/frequentroutes')
def frequentroutes():

    if g.email:
        
        cur = db.connection.cursor()
        cur.execute('''SELECT * FROM Routes where email: %s order by dateSearch desc limit 3''')
        rutas_list = cur.fetchall()
        
        dict_rutas = []
        ist_rutas = ["From", "To", "Type Car", "Load of the car", "Load"]

        for ruta in rutas_list:
            
            dict_rutas.append({
                "From" : ruta.from_ub,
                "To" : ruta.to_ub,
                "Type Car" : ruta.typeCar,
                "Load of the car" : ruta.typeLoad
        })
        
        return render_template('frequentroutes.html', email=current_user.email, dict_rutas=dict_rutas, list_rutas=list_rutas)
    
    else:
        return render_template('login.html')
    

    


@main.route('/delete')
def delete():
    return render_template('delete.html', name=current_user.name)




# 6- Página profile -----------------------------------------------
#------------------------------------------------------------------

@main.route('/profile2')
def profile2():

    car_list = ElectricCar.query.all()
    list_typeCar = []
    list_model = []

    for car in car_list:
        list_typeCar.append(car.brand)
        list_model.append(car.model)
        
    return render_template('profile2.html', email = current_user.email, name = current_user.name, lastName = current_user.lastName, typeCar = list_typeCar, typeModel = list_model)



@main.route('/ruta_test')
def ruta_test():

    ruta = main_route(tipo_programa = "ALL",
            marca_coche = "VOLKSWAGEN",
            modelo_coche = "ID3 PURE",
            origen = "Alicante Tren",
            destino = "A Corunia Bus"
    )

    return render_template('ruta_test.html', ruta=ruta)

