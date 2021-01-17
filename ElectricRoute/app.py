from flask import Flask, request, render_template, redirect, url_for, session, flash, Markup, send_from_directory
from flask_sqlalchemy import SQLAlchemy, inspect
from flask_login import UserMixin, login_required, LoginManager, login_user, logout_user, current_user
from flask_mail import Mail, Message
from sklearn.linear_model import LinearRegression
import base64
import plotly
import plotly.graph_objs as go
import plotly.figure_factory as ff
import numpy as np
import os
import pandas as pd
import random
import pulp as plp
import boto3
from io import StringIO, BytesIO
from botocore.client import Config
from werkzeug.utils import secure_filename
import json
import time
import pickle
import socket
from datetime import datetime
from app_init import app, simulation_dict
from funciones_BD import User, Simulation, db
from correo import mail


# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('Untitled-2.html')


#      app.run(debug="True", threaded=True)
     

import pandas as pd

df = pd.read_csv('PW_BI_Maestro.csv', sep= ';', encoding = 'unicode-escape')

