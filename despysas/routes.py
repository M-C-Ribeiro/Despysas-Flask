from despysas import app, db # aplicativo e banco de dados
from flask import flash, jsonify, redirect, render_template, request, url_for # modulos Flask
from sqlalchemy import extract
from despysas.models import Capitais, Categorias, Despesas, Users # modelos das tabelas 
from despysas.forms import CadastroFormUsuario, CadastroFormCategoria, CadastroFormCapital, CadastroFormDespesa, LoginForm, TabelaFiltrada # formularios para validacao
from flask_login import login_required, login_user, logout_user # controle do login do usuário
import pandas as pd # criação de dashboards
import plotly.express as px # plotagem de gráficos
import requests, json
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

@app.route('/') # decorator rota raiz
@login_required
def page_dashboard():

    # --------------- transformando as tabelas em dataframes ---------------
    categorias = db.session.query(Categorias.id, Categorias.nome, Categorias.descricao, Categorias.despesas).all() # buscando os valores
    df_categorias = pd.DataFrame(categorias, columns=["id", "nome", "descricao","despesa"]) # criando o dataframe

    capitais = db.session.query(Capitais.id, Capitais.nome, Capitais.valor, Capitais.data).all() # buscando os valores
    df_capitais = pd.DataFrame(capitais, columns=["id", "nome", "valor", "data_capitais"]) # criando o dataframe
    df_capitais['data_capitais'] = pd.to_datetime(df_capitais['data_capitais']) # converte o valor da coluna para um atributo válido, datetime
    df_capitais['mes'] = df_capitais['data_capitais'].dt.month

    despesas = db.session.query(Despesas.id, Despesas.nome, Despesas.valor, Despesas.descricao, Despesas.categoria, Despesas.data).all() # buscando os valores
    df_despesas = pd.DataFrame(despesas, columns=["id", "nome", "valor", "descricao", "categoria", "data_despesa"]) # criando o dataframe
    df_despesas['data_despesa'] = pd.to_datetime(df_despesas['data_despesa']) # converte o valor da coluna para um atributo válido, datetime
    df_despesas['mes'] = df_despesas['data_despesa'].dt.month

    df_completo = pd.merge(df_despesas, df_categorias, how="right", left_on='categoria', right_on='id', suffixes=('_despesa', '_categoria')) 
    df_completo['mes'] = df_completo['data_despesa'].dt.month
    df_completo = df_completo.loc[df_completo["despesa"]].drop_duplicates(subset="id_despesa")

    df_novo = pd.merge(df_despesas, df_capitais, on='mes', how='inner', suffixes=('_capital', '_despesa')).drop_duplicates(subset="id_despesa")

    # --------------- gráfico gastos por categoria ---------------
    fig = px.bar(df_completo, x='nome_categoria', y='valor', color='nome_categoria',
                labels={'valor': 'Valor', 'mes': 'Mês', 'nome_categoria': 'Categoria'},
                title='Valores por Categoria').update_layout(width=500, height=500)


    figura_gastos_categoria = fig.to_html(full_html=False)


    # --------------- gráfico capitais recebidos por mês ---------------

    df_capitais['mes'] = df_capitais['data_capitais'].dt.month
    fig = px.bar(df_capitais, x='mes', y='valor',color='mes', 
                 labels={'valor': 'Valor', 'mes': 'Mês'}, 
                 title='Valores por Mês').update_layout(width=500, height=500)

    entrada_mes = fig.to_html(full_html=False)


    # --------------- crescimento dos gastos e dos lucros ---------------
    # # df = pd.concat
    # fig = px.scatter(df_novo, x="mes", y=["capital", "despesas"], title="Capitais e Despesas")
    # capitais_despesa = fig.to_html(full_html=False)

    return render_template("dashboard.html", figura_gastos_categoria=figura_gastos_categoria, entrada_mes=entrada_mes)#, capitais_despesa=capitais_despesa) 


@app.route('/table', methods=['GET','POST']) # decorator rota table
@login_required
def page_table():
    form = TabelaFiltrada()

    if request.method == 'POST':
        mes = Capitais.query.filter_by(meses=form.meses.data).first()   
        print(mes)
        capital = Capitais.query.filter(extract("month", Capitais.data) == mes).all() # consulta em todas as linhas da tabela Capitais
        despesa = Despesas.query.all() # consulta em todas as linhas da tabela Despesas
        return render_template("table.html", capital=capital, despesa=despesa, form=form) 

    
    capital = Capitais.query.all() # consulta em todas as linhas da tabela Capitais    
    despesa = Despesas.query.all() # consulta em todas as linhas da tabela Despesas


    # lista = set([(mes.data.month) for mes in Capitais.query.all()]) # busca na
    return render_template("table.html", capital=capital, despesa=despesa, form=form) # renderiza o arquivo table.html com os parametros

@app.route('/filtro/<mes>')
def filtro(mes):
    linhas_filtradas = Capitais.query.filter_by(meses=mes).all()

    lista_capitais = []

    for capital in linhas_filtradas:
        obj_capital = {}
        obj_capital['id'] = capital.id
        obj_capital['nome'] = capital.nome
        obj_capital['valor'] = capital.valor

        lista_capitais.append(obj_capital)

    return jsonify({'capitais': lista_capitais})


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

    token = "v5y2BDgq6LykAjCHuubjBe"
    dash_app = Dash()

    # --------------- Gráfico de ações com maior crescimento ---------------
    url = f'https://brapi.dev/api/quote/list?sortBy=change&sortOrder=desc&limit=10&token={token}'
    req = requests.get(url) # requisição
    res = json.loads(req.text) #resposta
    df = pd.DataFrame(res['stocks']).drop_duplicates(subset="name") # transformando a resposta em um dataframe

    fig = px.bar(df, x="name", y="change",
                 color="sector",
                 labels={"name":"Ativo", "change":"Crescimento"}, 
                 title="Ações com maior crescimento")
    maior_crescimento = fig.to_html(full_html=False)

    # --------------- Gráfico da taxa de inflação do Brasil ---------------
    url = f'https://brapi.dev/api/v2/inflation?country=brazil&start=01/01/2022&end=01/01/2023&sortBy=date&sortOrder=asc&t'
    req = requests.get(url)
    res = json.loads(req.text)
    df = pd.DataFrame(res['inflation'])
    df['value'] = df['value'].astype(float)

    print(df['value'].dtypes)
    fig = px.line(df, x="date", y="value")
    fig.update_layout(title="Taxa de Inflação Jan. 2022 à Jan. 2023")
    fig.update_xaxes(title_text="Meses", showgrid=True, gridwidth=1, gridcolor='lightgray', showline=True, linewidth=1, linecolor='black')
    fig.update_yaxes(title_text="Taxa", showgrid=True, gridwidth=1, gridcolor='lightgray', showline=True, linewidth=1, linecolor='black')
    fig.add_trace(go.Scatter(x = df['date'], y = df['value']))
    inflacao = fig.to_html(full_html=False)

    return render_template('investimentos.html', maior_crescimento=maior_crescimento, inflacao=inflacao)