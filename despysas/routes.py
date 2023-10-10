from despysas import app, db # aplicativo e banco de dados
from flask import render_template, redirect, url_for, flash # modulos Flask
from despysas.models import Capitais, Despesas, Users # modelos das tabelas 
from despysas.forms import CadastroFormUsuario, CadastroFormCapital, CadastroFormDespesa, LoginForm # formularios para validacao
from flask_login import login_user
@app.route('/') # decorator rota raiz
def page_dashboard():
    return render_template("dashboard.html") # renderiza o arquivo dashboard.html

@app.route('/table') # decorator rota table
def page_table():
    capital = Capitais.query.all() # consulta em todas as linhas da tabela Capitais
    despesa = Despesas.query.all() # consulta em todas as linhas da tabela Despesas
    return render_template("table.html", capital=capital, despesa=despesa) # renderiza o arquivo table.html com os parametros

@app.route('/user') # decorator rota user
def page_user():    
    return render_template("user.html") # renderiza o arquivo user.html

@app.route('/cadastro', methods=['GET', "POST"]) # decorator rota cadastro de usuario
def page_cadastro():
    form = CadastroFormUsuario() # consulta informacoes do formulario de cadastro
    
    if form.validate_on_submit(): # verificacao das entradas no formulario
        usuario= Users(
            usuario = form.usuario.data,
            email = form.email.data,
            senha_crip = form.senha1.data
        )
        db.session.add(usuario) # prepara o envio dos dados
        db.session.commit() # envia para o bd
        return redirect(url_for('page_dashboard')) # retorna para a página dos dashboards
    
    if form.errors != {}: #verificacao de erros
        for err in form.errors.values():
            flash(f"Erro ao cadastrar usuário: {err}", category='danger')
    return render_template("cadastro.html", form=form) # renderiza o formulario

@app.route('/cadastro_capital', methods=['GET', "POST"]) # decorator rota cadastro de capital
def page_cadastro_capital():
    form = CadastroFormCapital() # consulta informacoes do formulario de cadastro de capital
    
    if form.validate_on_submit(): # verificacao das entradas no formulario
        capital= Capitais(
            nome = form.nome.data,
            valor = form.valor.data
        )
        db.session.add(capital) # prepara o envio dos dados
        db.session.commit() # envia para o bd
        return redirect(url_for('page_dashboard')) # retorna para a página dos dashboards
    
    if form.errors != {}: #verificacao de erros
        for err in form.errors.values():
            flash(f"Erro ao cadastrar usuário: {err}", category='danger')
    return render_template("cadastro_capital.html", form=form) # renderiza o formulario

@app.route('/cadastro_despesa', methods=['GET', "POST"])
def page_cadastro_despesa():
    form = CadastroFormDespesa() # consulta informacoes do formulario de cadastro de despesas

    if form.validate_on_submit(): # verificacao das entradas no formulario
        despesa= Despesas(
            nome = form.nome.data,
            valor = form.valor.data,
            descricao = form.descricao.data,
            categoria = form.categoria.data
        )
        db.session.add(despesa) # prepara o envio dos dados
        db.session.commit() # envia para o bd
        return redirect(url_for('page_dashboard')) # retorna para a página dos dashboards
    
    if form.errors != {}: #verificacao de erros
        for err in form.errors.values():
            flash(f"Erro ao cadastrar usuário: {err}", category='danger')
    return render_template("cadastro_despesa.html", form=form) # renderiza o formulario

@app.route('/login', methods=['GET','POST'])
def page_login():
    form = LoginForm() # consulta informacoes do formulario de cadastro de despesas

    if form.validate_on_submit(): # verificacao das entradas no formulario
        usuario_logado = Users.query.filter_by(usuario=form.usuario.data).first() # busca o usuario informado no bd
        if usuario_logado and usuario_logado.descript(senha_texto_livre=form.senha.data): #verificacao de erros
            login_user(usuario_logado)
            flash(f"Sucesso! Seu login é: {usuario_logado.usuario}", category="success")
            return redirect(url_for('page_dashboard'))
        else: flash(f"Usuário ou senha está(ão) incorreto(s)! Tente novamente.", category="danger")
    return render_template('login.html', form=form) # renderiza o formulario

@app.route('/investimentos')
def page_investimentos():
    return render_template('investimentos.html')