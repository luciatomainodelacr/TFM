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
from flask import Blueprint, Flask, render_template, request, redirect, url_for
from flask_login import UserMixin, login_required, LoginManager, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from . import db

# from forms import SignupForm

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)



# Se cargan las librerias
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
    email    = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])    
    submit   = SubmitField('Registrar')


# 2.- Página para logearse ----------------------------------------
#------------------------------------------------------------------

@main.route('/login', methods = ["GET", "POST"])
def login():
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        next = request.args.get('next', None)
        if next:
            return redirect(next)
        return redirect(url_for('index'))

    return render_template('login.html', form=form)



# 3.- Página register ---------------------------------------------
#------------------------------------------------------------------

@main.route('/register', methods = ["GET", "POST"])
def register():
    return render_template('register.html')


# 4.- Página forgot-password --------------------------------------
#------------------------------------------------------------------

@main.route('/password', methods = ["GET", "POST"])
def password():
    return render_template('password.html')



@main.route('/password1', methods = ["GET", "POST"])
def password1():
    return render_template('password1.html')


# 5.- Página index ------------------------------------------------
#------------------------------------------------------------------

@main.route('/index', methods = ["GET", "POST"])
def index():
    return render_template('index.html')



# 5.- Página ruta (mapa) ----------------------------------------
#------------------------------------------------------------------

@main.route('/Route', methods = ["GET", "POST"])
def route():
    return render_template('route.html')


# 6.- Página Rutas Frecuentes -------------------------------------
#------------------------------------------------------------------

@main.route('/rutasFrecuentes')
def rutasFrecuentes():
    return 'Rutas Frecuentes'



# 7.- Página profile -----------------------------------------------
#------------------------------------------------------------------

@main.route('/profile', methods = ['POST', 'GET'])
def profile():
    return render_template('profile.html')






