from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class RegistroForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Registrar')

class ContatoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    celular = StringField('Celular', validators=[DataRequired()])
    submit = SubmitField('Salvar Contato')

class MensagemForm(FlaskForm):
    texto = TextAreaField('Texto', validators=[DataRequired()])
    titulo = StringField('Título', validators=[DataRequired(), Length(max=100)])
    contato_id = SelectField('Contato', coerce=int)
    submit = SubmitField('Enviar Mensagem')
