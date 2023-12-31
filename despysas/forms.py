from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, SelectField
from wtforms.validators import Length, DataRequired, EqualTo, Email, InputRequired, ValidationError 
from despysas.models import Users, Categorias

class TabelaFiltrada(FlaskForm):
    meses = SelectField(label="Mês", choices=[], validators=[InputRequired(message='Por favor, selecione uma opção')]) 

class CapturaInvestimento(FlaskForm):
    acoes = SelectField(label="Ações", choices=[], validators=[InputRequired(message='Por favor, selecione uma opção')])
    investimento = FloatField(label="Investimento", validators=[DataRequired()])
    submit = SubmitField(label="Simular")

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
    nome = StringField(label="Título", validators=[Length(max=30), DataRequired()])
    valor = FloatField(label="Valor", validators=[DataRequired()])
    submit = SubmitField(label="Cadastrar")

class CadastroFormDespesa(FlaskForm):
    # Nao necessita validacao maior, devido a nao serem valores unicos
    nome = StringField(label="Título", validators=[Length(max=30), DataRequired()])
    valor = FloatField(label="Valor", validators=[DataRequired()])
    descricao = StringField(label="Descrição", validators=[Length(max=500), DataRequired()])

    categoria = SelectField(label="Selecione a Categoria", choices=[], validators=[DataRequired()])
    submit = SubmitField(label="Cadastrar")

class CadastroFormCategoria(FlaskForm):
    nome = StringField(label="Título", validators=[Length(max=30), DataRequired()])
    descricao = StringField(label="Descrição", validators=[Length(max=500), DataRequired()])
    submit = SubmitField(label="Cadastrar")

class EditaFormCapital(FlaskForm):
    # Nao necessita validacao maior, devido a nao serem valores unicos
    id = IntegerField(label="ID do cadastro:", validators=[DataRequired()])
    nome = StringField(label="Título", validators=[Length(max=30), DataRequired()])
    valor = FloatField(label="Valor", validators=[DataRequired()])
    submit = SubmitField(label="Atualizar")

class EditaFormDespesa(FlaskForm):
    # Nao necessita validacao maior, devido a nao serem valores unicos
    id = IntegerField(label="ID do cadastro:", validators=[DataRequired()])
    nome = StringField(label="Título", validators=[Length(max=30), DataRequired()])
    valor = FloatField(label="Valor", validators=[DataRequired()])
    descricao = StringField(label="Descrição", validators=[Length(max=500), DataRequired()])

    categoria = SelectField(label="Selecione a Categoria", choices=[], validators=[DataRequired()])
    submit = SubmitField(label="Atualizar")

class EditaFormCategoria(FlaskForm):
    id = IntegerField(label="ID do cadastro:", validators=[DataRequired()])
    nome = StringField(label="Título", validators=[Length(max=30), DataRequired()])
    descricao = StringField(label="Descrição", validators=[Length(max=500), DataRequired()])
    submit = SubmitField(label="Atualizar")

class LoginForm(FlaskForm):
    usuario = StringField(label="Usuário:", validators=[DataRequired()])
    senha = PasswordField(label="Senha:", validators=[DataRequired()])
    submit = SubmitField(label="Log In")

class Deletar(FlaskForm):
    id = IntegerField(label="ID do cadastro:", validators=[DataRequired()])
    tabela = SelectField(label="Tipo de Dado:", choices=[], validators=[InputRequired(message='Por favor, selecione uma opção')])
    submit = SubmitField(label="Excluir")