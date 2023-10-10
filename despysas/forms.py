from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError 
from despysas.models import Users
    
class CadastroFormUsuario(FlaskForm):
    def validate_username(self, check_user):
        user = Users.query.filter_by(usuario=check_user.data).first()
        if user:
            raise ValidationError("Usuário já existe! Cadastre outro nome de usuário")
        
    def validate_mail(self, check_mail):
        email = Users.query.filter_by(email=check_mail.data).first()
        if email:
            raise ValidationError("E-mail já cadastradi! Cadastre outro válido.")
        
    usuario = StringField(label="Username:", validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label="E-mail:", validators=[Email(), DataRequired()])
    senha1 = PasswordField(label="Senha:", validators=[Length(min=6), DataRequired()])
    senha2 = PasswordField(label="Confirme sua Senha:", validators=[EqualTo('senha1'), DataRequired()])
    submit = SubmitField(label="Cadastrar")

class CadastroFormCapital(FlaskForm):
    # Nao necessita validacao maior, devido a nao serem valores unicos
    nome = StringField(label="Título", validators=[Length(max=30)])
    valor = FloatField(label="Valor")
    submit = SubmitField(label="Cadastrar")

class CadastroFormDespesa(FlaskForm):
    # Nao necessita validacao maior, devido a nao serem valores unicos
    nome = StringField(label="Título", validators=[Length(max=30)])
    valor = FloatField(label="Valor")
    descricao = StringField(label="Descrição", validators=[Length(max=500)])
    categoria = IntegerField(label="ID da Categoria")
    submit = SubmitField(label="Cadastrar")

class LoginForm(FlaskForm):
    usuario = StringField(label="Usuário:", validators=[DataRequired()])
    senha = PasswordField(label="Senha:", validators=[DataRequired()])
    submit = SubmitField(label="Log In")