# =============================================================================
#  auth.py
# =============================================================================


# Se cargan las librerias
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)



# 1.- Página login ------------------------------------------------
#------------------------------------------------------------------

@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember) 
    return redirect(url_for('main.index'))


# 2.- Página signup ------------------------------------------------
#------------------------------------------------------------------

@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():

    email    = request.form.get('email')
    name     = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))



# 3.- Página logout ------------------------------------------------
#------------------------------------------------------------------

@auth.route('/logout')
def logout():
    return 'Logout'


# 3. Pagina profile  ------------------------------------------------
#------------------------------------------------------------------
@auth.route('/profile')
def profile():
    return render_template('profile.html')

@auth.route('/profile', methods=['GET'])
def profile_get():

    email    = request.form.get('email')
    name     = request.form.get('name')
    last_name = request.form.get('last_name')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    return redirect(url_for('profile'),name=current_user.name, email=current_user.email, last_name=current_user.last_name)


# 3. Pagina Rutas Frecuentes  ------------------------------------------------
#------------------------------------------------------------------
@auth.route('/frequentroutes')
def frequentroutes():
    return render_template('frequentroutes.html')

@auth.route('/frequentroutes', methods=['GET'])
def frequentroutes_get():

    from_car    = request.form.get('from_car')
    to     = request.form.get('to')
    typecar = request.form.get('typecar')
    load = request.form.get('load')

    user = Route.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    return redirect(url_for('profile'),from_car=current_user.from_car, to=current_user.to, typecar=current_user.typecar, load=current_user.load)