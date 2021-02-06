# =============================================================================
#  models.py
# =============================================================================


# Se cargan las librerias
from flask_login import UserMixin, login_user, logout_user, login_required
from datetime import datetime
from . import db

# Se define la clase User
class User_2(UserMixin, db.Model):

    id       = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    email    = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name     = db.Column(db.String(1000))
    lastName = db.Column(db.String(100))
    typeCar  = db.Column(db.String(100))

class Route(UserMixin, db.Model):

    __tablename__ = 'Route'
    
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    from_ub = db.Column(db.String(1000))
    to_ub = db.Column(db.String(1000)) 
    typeCar = db.Column(db.String(1000))  
    typeLoad = db.Column(db.String(1000))
    dateSearch = db.Column(db.DateTime(6)) 


