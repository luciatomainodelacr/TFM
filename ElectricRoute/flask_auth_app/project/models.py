# =============================================================================
#  models.py
# =============================================================================


# Se cargan las librerias
from flask_login import UserMixin, login_user, logout_user, login_required
from . import db

# Se define la clase User
class User(UserMixin, db.Model):

    id       = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    email    = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name     = db.Column(db.String(1000))
    lastName = db.Column(db.String(100))
    typeCar  = db.Column(db.String(100))

class Route(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    from_car = db.Column(db.String(100))
    to = db.Column(db.String(1000)) 
    type_car = db.Column(db.String(1000))  
    load = db.Column(db.String(1000))   


