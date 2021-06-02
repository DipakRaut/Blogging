from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os
# >>> db.create_all() it will create the databases
# 17:10 ----> 4
# url_for is a function that will find a exact location of routes for us 
# instained flask application
app = Flask(__name__) # creating the app variable and setting this to an instance of flask class name is same as main when you run the app
# app.config["SECRET_KET"] = "8f8d320eb237bed38368d245d4163ec3bd"
SECRET_KEY = os.urandom(32)	
app.config['SECRET_KEY'] = SECRET_KEY
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# to setting this location we need to set this as a configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # we are giving the URL for storing the database i.e location of database
db = SQLAlchemy(app) # Creating the database instances
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login" # this view we have passed here is the function name of the route so its the same thing we have passed for the url_for function
login_manager.login_message_category = "info" # this is just used to show the flashed message on the log in page in blue i.e "info" 
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "dipakraut114@gmail.com"
app.config["MAIL_PASSWORD"] = "Raju1443@1443Tilo"	
mail = Mail(app) # initilize the Extension

from blog import routes 