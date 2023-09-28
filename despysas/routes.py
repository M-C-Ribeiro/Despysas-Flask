from despysas import app, db
from flask import render_template, redirect, url_for, flash
from despysas.models import Capitais, Despesas, Users
from despysas.forms import CadastroFormUsuario, CadastroFormCapital, CadastroFormDespesa

@app.route('/') # decorator rota raiz
def page_dashboard():
    return render_template("dashboard.html") # renderiza o arquivo dashboard.html

@app.route('/table') # decorator rota table
def page_table():
    capital = Capitais.query.all()
    despesa = Despesas.query.all()
    return render_template("table.html", capital=capital, despesa=despesa) # renderiza o arquivo table.html com os parametros

@app.route('/user') # decorator rota user
def page_user():    
    return render_template("user.html") # renderiza o arquivo user.html

@app.route('/cadastro', methods=['GET', "POST"])
def page_cadastro():
    form = CadastroFormUsuario()
    
    if form.validate_on_submit():
        usuario= Users(
            usuario = form.usuario.data,
            email = form.email.data,
            senha = form.senha1.data
        )
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('page_dashboard'))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f"Erro ao cadastrar usuário: {err}", category='danger')
    return render_template("cadastro.html", form=form)

@app.route('/cadastro_capital', methods=['GET', "POST"])
def page_cadastro_capital():
    form = CadastroFormCapital()
    if form.validate_on_submit():
        capital= Capitais(
            nome = form.nome.data,
            valor = form.valor.data
        )
        db.session.add(capital)
        db.session.commit()
        return redirect(url_for('page_dashboard'))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f"Erro ao cadastrar usuário: {err}", category='danger')
    return render_template("cadastro_capital.html", form=form)

@app.route('/cadastro_despesa', methods=['GET', "POST"])
def page_cadastro_despesa():
    form = CadastroFormDespesa()
    if form.validate_on_submit():
        despesa= Capitais(
            nome = form.nome.data,
            valor = form.valor.data
        )
        db.session.add(despesa)
        db.session.commit()
        return redirect(url_for('page_dashboard'))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f"Erro ao cadastrar usuário: {err}", category='danger')
    return render_template("cadastro_despesa.html", form=form)