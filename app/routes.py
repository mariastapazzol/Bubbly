from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from .models import db, Usuario, Contato, Mensagem
from .forms import LoginForm, RegistroForm, ContatoForm, MensagemForm

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and check_password_hash(usuario.senha, form.senha.data):
            login_user(usuario)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login inválido')
    return render_template('login.html', form=form)


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistroForm()
    if form.validate_on_submit():
        hashed = generate_password_hash(form.senha.data)
        user = Usuario(nome=form.nome.data, email=form.email.data, senha=hashed)
        db.session.add(user)
        db.session.commit()
        flash('Conta criada!')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@main.route('/contatos', methods=['GET', 'POST'])
@login_required
def contatos():
    form = ContatoForm()
    if form.validate_on_submit():
        contato = Contato(
            nome=form.nome.data,
            email=form.email.data,
            celular=form.celular.data,
            dono=current_user
        )
        db.session.add(contato)
        db.session.commit()
        flash("Contato salvo com sucesso.")
        return redirect(url_for('main.contatos'))

    contatos = Contato.query.filter_by(dono=current_user).all()
    return render_template('contatos.html', form=form, contatos=contatos)


@main.route('/contatos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_contato(id):
    contato = Contato.query.get_or_404(id)
    if contato.dono != current_user:
        flash("Acesso negado.")
        return redirect(url_for('main.contatos'))

    form = ContatoForm(obj=contato)
    if form.validate_on_submit():
        contato.nome = form.nome.data
        contato.email = form.email.data
        contato.celular = form.celular.data
        db.session.commit()
        flash("Contato atualizado com sucesso.")
        return redirect(url_for('main.contatos'))

    return render_template('editar_contato.html', form=form, contato=contato)


@main.route('/contatos/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_contato(id):
    contato = Contato.query.get_or_404(id)
    if contato.dono != current_user:
        flash("Acesso negado.")
        return redirect(url_for('main.contatos'))

    db.session.delete(contato)
    db.session.commit()
    flash("Contato excluído com sucesso.")
    return redirect(url_for('main.contatos'))


@main.route('/mensagens', methods=['GET', 'POST'])
@login_required
def mensagens():
    form = MensagemForm()
    form.contato_id.choices = [(c.id, c.nome) for c in Contato.query.filter_by(dono=current_user)]

    if form.validate_on_submit():
        msg = Mensagem(
            titulo=form.titulo.data,
            texto=form.texto.data,
            autor=current_user,
            contato_id=form.contato_id.data
        )
        db.session.add(msg)
        db.session.commit()
        flash("Mensagem enviada.")
        return redirect(url_for('main.mensagens'))

    mensagens = Mensagem.query.filter_by(autor=current_user).order_by(Mensagem.data_envio.desc()).all()
    return render_template('mensagens.html', form=form, mensagens=mensagens)
