# =============================================================================
#  models.py
# =============================================================================


# Se cargan las librerias
from flask_login import UserMixin
from . import db

# Se define la clase User
class User(UserMixin, db.Model):

    id       = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    email    = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name     = db.Column(db.String(1000))
    lastName = db.Column(db.String(100))
    typeCar  = db.Column(db.String(100))


