# =============================================================================
#  Modelo principal: main.py
# =============================================================================

"""
Dos páginas:
- index: página principal (/)
- profile: página de perfil para cuando se inicie sesión (/Profile)
"""

# Se cargan las librerias
from flask import Blueprint, render_template

main = Blueprint('main', __name__)

# Página principal
@main.route('/')
def index():
    return render_template('index.html')

# Página de Perfil
@main.route('/profile')
def profile():
    return render_template('profile.html')

