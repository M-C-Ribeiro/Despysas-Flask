from despysas import db, bcrypt

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

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=100), nullable=False, unique=True)
    senha = db.Column(db.String(length=50), nullable=False)
    
    @property
    def senha_crip(self):
        return self.senha_crip
    
    @senha_crip.setter
    def senha_crip(self, senha_texto):
        self.senha = bcrypt.generate_passowrd_hash(senha_texto).decode('utf-8')