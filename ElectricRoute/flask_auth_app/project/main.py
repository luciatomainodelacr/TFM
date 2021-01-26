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
from flask_sqlalchemy import SQLAlchemy
from . import db



main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)




# 2.- Página para logearse ----------------------------------------
#------------------------------------------------------------------

@main.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        next = request.args.get('next', None)
        if next:
            return redirect(url_for('next'))
        return redirect(url_for('index'))

    return render_template('login.html')


# 3.- Página index ------------------------------------------------
#------------------------------------------------------------------

@main.route('/index', methods = ["GET", "POST"])
def index():
    return render_template('index.html')



# 4.- Página ruta (mapa) ----------------------------------------
#------------------------------------------------------------------

@main.route('/Route', methods = ["GET", "POST"])
def route():
    return render_template('route.html')


# 5.- Página Rutas Frecuentes -------------------------------------
#------------------------------------------------------------------

@main.route('/rutasFrecuentes')
def rutasFrecuentes():
    return 'Rutas Frecuentes'



# 6.- Página profile -----------------------------------------------
#------------------------------------------------------------------

@main.route('/profile', methods = ['POST', 'GET'])
def profile():
    return render_template('profile.html')


# 6.- Olvida Contraeña parte 1-----------------------------------------------
#------------------------------------------------------------------
@main.route("/forgot-password", methods=["POST"])
def pwresetrq_post():
    if session.query(User).filter_by(email=request.form["email"]).first():
        user = session.query(User).filter_by(email=request.form["email"]).one()
        # check if user already has reset their password, so they will update
        # the current key instead of generating a separate entry in the table.
        if session.query(PWReset).filter_by(user_id = user.id).first():
            pwalready = session.query(PWReset).filter_by(user_id = user.id).first()
	# if the key hasn't been used yet, just send the same key.
            if pwalready.has_activated == False:
                pwalready.datetime = datetime.now()
                key = pwalready.reset_key
            else:    
                key = keygenerator.make_key()
                pwalready.reset_key = key
                pwalready.datetime = datetime.now()
                pwalready.has_activated = False
        else:  
            key = keygenerator.make_key()
            user_reset = PWReset(reset_key=key, user_id=user.id)
            session.add(user_reset)
            session.commit()
	    return redirect(url_for("index"))
    else:
        flash("Your email was never registered.", "danger")
        return redirect(url_for("index"))

# 7.- Olvida Contraeña parte 2-----------------------------------------------
#------------------------------------------------------------------
import uuid

def make_key():
    return uuid.uuid4()

@main.route("/forgot-password", methods=["GET"])
def pwreset_get(id):
    key = id
    pwresetkey = session.query(PWReset).filter_by(reset_key=id).one()
    generated_by = datetime.utcnow().replace(tzinfo=pytz.utc) - timedelta(hours=24)
    if pwresetkey.has_activated is True:
        flash ("You already reset your password with the URL you are using." +
              "If you need to reset your password again, please make a" +
              " new request here.", "danger")
        return redirect(url_for("password"))
    if pwresetkey.datetime.replace(tzinfo=pytz.utc) < generated_by:
        flash("Your password reset link expired.  Please generate a new one" +
              " here.", "danger")
        return redirect(url_for("password"))
    return render_template('index.html', id=key)

@main.route("/forgot-password", methods=["POST"])
def pwreset_post(id):
    if request.form["password"] != request.form["password2"]:
        flash("Your password and password verification didn't match."
          , "danger")
        return redirect(url_for("password", id=id))
    if len(request.form["password"]) < 8:
        flash("Your password needs to be at least 8 characters", "danger")
        return redirect(url_for("password", id=id))
    user_reset = session.query(PWReset).filter_by(reset_key=id).one()
    try:
        exists(session.query(User).filter_by(id = user_reset.user_id)
               .update({'password':
                        generate_password_hash(request.form["password"])}))
        session.commit(exists)
    except IntegrityError:
        flash("Something went wrong", "danger")
        session.rollback()
        return redirect(url_for("index"))
    user_reset.has_activated = True
    session.commit()
    flash("Your new password is saved.", "success")
    return redirect(url_for("index"))
