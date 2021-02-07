# =============================================================================
#  auth.py
# =============================================================================


# Se cargan las librerias
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from flask_mysqldb import MySQL
import mysql.connector
import MySQLdb.cursors 
import re 
from . import db



auth = Blueprint('auth', __name__)



# 1.- Página login ------------------------------------------------
#------------------------------------------------------------------

@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods =['GET', 'POST']) 
def login_post(): 

    # Se inicializa el mensaje que mostrará al usuario
    msg = '' 

    if request.method == 'POST' and 'email' in request.form and 'password' in request.form: 

        email = request.form['email'] 
        password = request.form['password'] 

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM users WHERE email = % s AND password = % s', (email, password, )) 
        user = cursor.fetchone() 

        if user: 
            session['loggedin'] = True
            session['id']       = user['id'] 
            session['email'] = user['email'] 

            # Mensaje de Loggin correcto
            msg = 'Logged in successfully !'

            return render_template('index.html', msg = msg) 
        else: 
            msg = 'Incorrect email / password !'

    return render_template('login.html', msg = msg)

 
 
 
 # 2.- Página signup ------------------------------------------------
 #-------------------------------------------------------------------

@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods =['GET', 'POST']) 
def signup_post(): 

    # Se inicializa el mensaje que mostrará al usuario
    msg = '' 

    if request.method == 'POST' and 'email' in request.form and 'username' in request.form and 'password' in request.form and 'lastName' in request.form and 'brandCar' in request.form and 'modelCar' in request.form :

        email    = request.form['email']
        username = request.form['username']
        password = request.form['password']
        lastName = request.form['lastName']
        brandCar = request.form['brandCar']
        modelCar = request.form['modelCar']
        

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM users WHERE email = % s', (email, )) 
        user = cursor.fetchone() 

        if user: 
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username): 
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email: 
            msg = 'Please fill out the form !'
        else: 
            cursor.execute('INSERT INTO users VALUES (NULL, % s, % s, % s, % s, % s, $ s)', (email, username, password, lastName, brandCar, modelCar)) 
            mysql.connection.commit() 
            msg = 'You have successfully registered !'

    elif request.method == 'POST': 
        msg = 'Please fill out the form!'

    return render_template('signup.html', msg = msg) 
 
  




# 3.- Página logout ------------------------------------------------
#-------------------------------------------------------------------
 
@auth.route('/logout')
def logout():
    return 'Logout'