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
from . import db



# Se define la clase
class User(UserMixin, db.Model):

    id       = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    email    = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name     = db.Column(db.String(1000))




class Ruta(UserMixin, db.Model):

    __tablename__ = 'ruta'

    id            = db.Column(db.Integer, primary_key=True)
    email         = db.Column(db.String(100))
    OrigenName    = db.Column(db.String(100))
    DestName      = db.Column(db.String(100))


    def __repr__(self):
        return f'<User {self.email}>'


    @staticmethod
    def get_by_origen(email):
        return Ruta.query.get(OrigenName)

    @staticmethod
    def get_by_destino(DestName):
        return Ruta.query.get(DestName)
        
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    

