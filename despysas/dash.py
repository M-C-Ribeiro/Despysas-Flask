from despysas import app, db # aplicativo e banco de dados
from despysas.models import Capitais, Despesas
import pandas as pd
import flask_sqlalchemy

df = Capitais.query.all()
print(df)