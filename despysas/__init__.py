from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy() # instancia a criacao do bd
app = Flask(__name__) # define o programa flask
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///despysas.db" # define o nome do bd
app.config["SECRET_KEY"] = "e45f77756f254708783c156b"
db.init_app(app) # inicia o banco
bcrypt = Bcrypt(app)

from despysas import routes