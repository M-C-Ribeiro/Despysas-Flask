from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy() # instancia a criacao do bd
login_manager = LoginManager() # instanciacao da biblioteca
app = Flask(__name__) # define o programa flask
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///despysas.db" # define o nome do bd
app.config["SECRET_KEY"] = "e45f77756f254708783c156b"
db.init_app(app) # inicia o banco
bcrypt = Bcrypt(app) # instancia a biblioteca com acesso ao aplicativo
login_manager.init_app(app) # inicializa o login manager
login_manager.login_view = "page_login"
login_manager.login_message = "Por favor, faça login" 

from despysas import routes