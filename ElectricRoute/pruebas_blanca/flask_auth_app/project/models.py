# =============================================================================
#  Modelo de usuario: models.py
# =============================================================================

"""
Se guarda la información para cada usuario: id, email, password y name
"""

# Se cargan las librerias
from project import db, create_app
db.create_all(app=create_app())


# Clase User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))