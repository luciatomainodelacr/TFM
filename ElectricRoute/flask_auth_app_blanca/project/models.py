# =============================================================================
#  models.py
# =============================================================================

"""
   Una vez que se ha establecido la configuración del objeto SQLAlchemy (fichero
    __init__.py), al cuál hemos llamado db, el siguiente paso es actualizar el 
    modelo User para que herede de la clase Model. Esto creará la equivalencia 
    entre la tabla user de la base de datos y la clase User.

    Análogo para el resto de tablas de la base de datos

"""

# Se cargan las librerias
from flask_login import UserMixin
from datetime import datetime
from . import db


# 1. Clase User ---------------------------------------------------
#------------------------------------------------------------------
class User(UserMixin, db.Model):

    id       = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    email    = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name     = db.Column(db.String(1000))
    lastName = db.Column(db.String(100))
    typeCar  = db.Column(db.String(100))
    


# 2. Clase Route --------------------------------------------------
#------------------------------------------------------------------

class Route(UserMixin, db.Model):
    
    __tablename__ = 'Route'
    
    id          = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email       = db.Column(db.String(100), unique=True)
    from_ub     = db.Column(db.String(1000))
    to_ub       = db.Column(db.String(1000)) 
    typeCar     = db.Column(db.String(1000))  
    typeLoad    = db.Column(db.String(1000))
    dateSearch  = db.Column(db.DateTime(6)) 



# 3. Clase ciudades -----------------------------------------------
#------------------------------------------------------------------
class ciudades(UserMixin, db.Model):

    __tablename__ = 'ciudades'

    id            = db.Column(db.String(100), primary_key=True, nullable=False, unique=True)
    provincia     = db.Column(db.String(100))
    Direccion     = db.Column(db.String(100))
    Latitud       = db.Column(db.String(100))
    Longitud      = db.Column(db.String(100))
    Coordenadas   = db.Column(db.String(100))

   
    def __repr__(self):
        return '<Ciudad {}>'.format(self.username)


# 4. Clase ElectricCar --------------------------------------------
#------------------------------------------------------------------

class ElectricCar(UserMixin, db.Model):
    
    __tablename__ = 'ElectricCar'

    brand           =  db.Column(db.Integer, primary_key=True)
    model           = db.Column(db.String(100))
    range_km        = db.Column(db.String(100))
    efficiency_whkm = db.Column(db.String(100))
    fastcharge_kmh  = db.Column(db.String(100))
    rapidcharge     = db.Column(db.String(100))
    plugtype = battery_capacity = db.Column(db.String(100))

