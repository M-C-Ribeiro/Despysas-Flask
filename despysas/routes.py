from despysas import app, db # aplicativo e banco de dados
from flask import render_template, redirect, url_for, flash # modulos Flask
from despysas.models import Categorias, Capitais, Despesas, Users # modelos das tabelas 
from despysas.forms import CadastroFormUsuario, CadastroFormCategoria, CadastroFormCapital, CadastroFormDespesa, LoginForm # formularios para validacao
from flask_login import login_user, logout_user
import pandas as pd
import plotly.express as px


@app.route('/') # decorator rota raiz
def page_dashboard():

    # --------------- transformando as tabelas em dataframes ---------------
    categorias = db.session.query(Categorias.id, Categorias.nome, Categorias.descricao, Categorias.despesas).all() # buscando os valores
    df_categorias = pd.DataFrame(categorias, columns=["id", "nome", "descricao","despesa"]) # criando o dataframe

    capitais = db.session.query(Capitais.id, Capitais.nome, Capitais.valor, Capitais.data).all() # buscando os valores
    df_capitais = pd.DataFrame(capitais, columns=["id", "nome", "valor", "data_capitais"]) # criando o dataframe
    df_capitais['data_capitais'] = pd.to_datetime(df_capitais['data_capitais'])

    despesas = db.session.query(Despesas.id, Despesas.nome, Despesas.valor, Despesas.descricao, Despesas.categoria, Despesas.data).all() # buscando os valores
    df_despesas = pd.DataFrame(despesas, columns=["id", "nome", "valor", "descricao", "categoria", "data_despesa"])
    df_despesas['data_despesa'] = pd.to_datetime(df_despesas['data_despesa'])

    df_completo = pd.merge(df_despesas, df_categorias, how="right", left_on='categoria', right_on='id', suffixes=('_despesa', '_categoria'))
    df_completo.drop_duplicates(subset="id_despesa")
    # Extrair o mês da data e adicionar como uma nova coluna no DataFrame
    df_completo['mes'] = df_completo['data_despesa'].dt.month
    df_completo = df_completo.loc[df_completo["despesa"]]

    # Criar o gráfico Plotly Express
    fig = px.bar(df_completo, x='nome_categoria', y='valor', color='nome_categoria',
                labels={'valor': 'Valor', 'mes': 'Mês', 'nome_categoria': 'Categoria'},
                title='Valores por Categoria').update_layout(width=400, height=400)
    

    # Converter o gráfico Plotly para HTML
    figura_gastos_categoria = fig.to_html(full_html=False)


    # --------------- gráfico capitais recebidos por mês ---------------

    df_capitais['mes'] = df_capitais['data_capitais'].dt.month
    fig = px.bar(df_capitais, x='mes', y='valor',color='mes', 
                 labels={'valor': 'Valor', 'mes': 'Mês'}, 
                 title='Valores por Mês').update_layout(width=400, height=400)

    entrada_mes = fig.to_html(full_html=False)

    return render_template("dashboard.html", figura_gastos_categoria=figura_gastos_categoria, entrada_mes=entrada_mes) 

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

@app.route('/cadastro_categoria', methods=['GET', 'POST'])
def page_cadastro_categoria():
    form = CadastroFormCategoria() # consulta informacoes do formulario de cadastro de capital
    
    if form.validate_on_submit(): # verificacao das entradas no formulario
        categoria= Categorias(
            nome = form.nome.data,
            descricao = form.descricao.data
        )
        db.session.add(categoria) # prepara o envio dos dados
        db.session.commit() # envia para o bd
        return redirect(url_for('page_dashboard')) # retorna para a página dos dashboards
    
    if form.errors != {}: #verificacao de erros
        for err in form.errors.values():
            flash(f"Erro ao cadastrar categoria: {err}", category='danger')
    return render_template("cadastro_categoria.html", form=form) # renderiza o formulario

@app.route('/cadastro_capital', methods=['GET', 'POST']) # decorator rota cadastro de capital
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
            flash(f"Erro ao cadastrar capital: {err}", category='danger')
    return render_template("cadastro_capital.html", form=form) # renderiza o formulario

@app.route('/cadastro_despesa', methods=['GET', 'POST'])
def page_cadastro_despesa():
    form = CadastroFormDespesa() # consulta informacoes do formulario de cadastro de despesas
    form.categoria.choices = [(0,'Selecione uma categoria')]+[(cat.id, cat.nome) for cat in Categorias.query.all()]

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
            flash(f"Erro ao cadastrar despesa: {err}", category='danger')
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

@app.route('/logout')
def page_logout():
    logout_user()
    flash("Usuário desconectado", category="info")
    return redirect(url_for("page_dashboard"))

@app.route('/investimentos')
def page_investimentos():
    return render_template('investimentos.html')