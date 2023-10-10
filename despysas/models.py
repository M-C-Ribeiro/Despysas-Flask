from despysas import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Modelo da tabela
class Categorias(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(length=30), nullable=False)
    descricao = db.Column(db.String(length=500), nullable=False)
    despesas = db.relationship('Despesas', backref='categoria_despesas', lazy=True)
     
class Despesas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(length=30), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(length=500), nullable=False)
    categoria = db.Column(db.Integer, db.ForeignKey('categorias.id'))

class Capitais(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(length=30), nullable=False)
    valor = db.Column(db.Float, nullable=False)

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=100), nullable=False, unique=True)
    senha = db.Column(db.String(length=50), nullable=False)
    
    @property # decorator para retornar o valor da senha 
    def senha_crip(self):
        return self.senha_crip
    
    @senha_crip.setter # decorator executado apos valor ser informado para senha_crip, criptografa a senha informada
    def senha_crip(self, senha_texto):
        self.senha = bcrypt.generate_password_hash(senha_texto).decode('utf-8')

    def descript(self, senha_texto_livre): # funcao para comparar a senha informada bate com a criptografada
        return bcrypt.check_password_hash(self.senha, senha_texto_livre)