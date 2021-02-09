# =============================================================================
#  auth.py
# =============================================================================


# Se cargan las librerias
from flask import Blueprint, render_template, redirect, url_for, request, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from flask_mysqldb import MySQL
import MySQLdb.cursors 
import mysql.connector
import re 
import flask_login
from . import db



auth = Blueprint('auth', __name__)

@auth.before_request
def before_request():
   g.email = None
   if 'email' in session:
       g.email = session['email']
 


# 1.- Página login ------------------------------------------------
#------------------------------------------------------------------

@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['GET', 'POST'])
def login_post():
    
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form: 

        email    = request.form['email'] 
        password = request.form['password'] 

        # Consulta a la bbdd
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM users WHERE email = % s AND password = % s', (email, password, )) 
        user = cursor.fetchone()


        if user: 
            session['loggedin'] = True
            session['id']       = user['id'] 
            session['email']    = user['email']
            session['username'] = user['username']
            session['lastName'] = user['lastName']
            session['brandCar'] = user['brandCar']
            session['modelCar'] = user['modelCar']
            session['connect']  = True
            username =  user['username']

            flash('Logged in successfully !')
            
            return render_template('index.html', email=email, name = username)
            
        else:
            flash('Incorrect email / password !')
            return redirect(url_for('auth.login'))
    
    return redirect(url_for('main.index'))




# 2.- Página signup ------------------------------------------------
#------------------------------------------------------------------

@auth.route('/signup')
def signup():

    # Consulta a la bbdd ElectricCar
    cur = db.connection.cursor()
    cur.execute('''SELECT * FROM ElectricCar''')
    electricCar_list = cur.fetchall()

    # Se inicializan dos listas para las marcas y los modelos de coche
    list_brand = []
    list_model = []

    for coche in electricCar_list:
        list_brand.append(coche[0])
        list_model.append(coche[1])
            
    return render_template('signup.html', list_brand = list_brand, list_model = list_model)




# 2.- Página signup ------------------------------------------------
#------------------------------------------------------------------

@auth.route('/signup',methods =['GET', 'POST'])
def signup_post():

    if request.method == 'POST' and ('email' != '') and ('email' in request.form and 'username' in request.form and 'password' in request.form and 'lastName' in request.form and 'mySelectBrand' in request.form and 'mySelectModel' in request.form): 

        email    = request.form['email']
        username = request.form['username']
        password = request.form['password']
        lastName = request.form['lastName']
        brandCar = request.form.get('mySelectBrand')
        modelCar = request.form.get('mySelectModel')

        print(brandCar)

        # Consulta a la bbdd users 
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = % s', (email, )) 
        user = cursor.fetchone()

        # Consulta a la bbdd ElectricCar
        cur = db.connection.cursor()
        cur.execute('''SELECT * FROM ElectricCar''')
        electricCar_list = cur.fetchall()

        # Se inicializan dos listas para las marcas y los modelos de coche
        list_brand = []
        list_model = []

        for coche in electricCar_list:
            list_brand.append(coche[0])
            list_model.append(coche[1])

            
        # Comprobaciones registro de usuario
        if user: 
            flash('Account already exists !')
            return redirect(url_for('auth.login'))

        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
            flash('Invalid email address !')
        elif not re.match(r'[A-Za-z0-9]+', username): 
            flash('Username must contain only characters and numbers !')
        elif not username or not password or not email or not lastName or not brandCar or not modelCar: 
            flash('Please fill out the form !')
            return redirect(url_for('auth.signup'))
        else: 
            cursor.execute('INSERT INTO users VALUES (NULL, % s, % s, % s,  % s, % s, % s)', (email, username, password, lastName, brandCar, modelCar)) 
            db.connection.commit() 
            flash('You have successfully registered !')  
            return redirect(url_for('auth.login')) 
    
    
    elif request.method == 'POST' and ('email' != '' and 'username' != '' and 'password' != '' and 'lastName' != '' and 'brandCar' != '' and 'modelCar' != '') :
        flash('Please fill out the form!')

        return redirect(url_for('auth.signup'))

    return redirect(url_for('auth.signup'))




# 3.- Página logout ------------------------------------------------
#------------------------------------------------------------------

@auth.route('/logout')
def logout():
    session.clear()
    return 'Logout'

    