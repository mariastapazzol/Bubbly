from . import db
from flask_login import UserMixin
from datetime import datetime
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(150), unique=True)
    senha = db.Column(db.String(60))
    contatos = db.relationship('Contato', backref='dono', lazy=True)
    mensagens = db.relationship('Mensagem', backref='autor', lazy=True)

class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(120))
    celular = db.Column(db.String(20))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False) 
    texto = db.Column(db.Text)
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    contato_id = db.Column(db.Integer, db.ForeignKey('contato.id'))
