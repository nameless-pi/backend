'''Modelos, feitos usando SQLAlchemy ORM, referentes à modelagem da base de dados.'''

__author__ = 'Gabriel Cordeiro'

from passlib.apps import custom_app_context as pwd_context
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class CRUD():
	def add(self, resource):
		db.session.add(resource)
		return db.session.commit()

	def update(self):
		return db.session.commit()

	def delete(self, resource):
		db.session.delete(resource)
		return db.session.commit()


class Admin(db.Model, CRUD):
	__tablename__ = "admin"

	id = db.Column(db.Integer, primary_key=True)
	login = db.Column(db.String(80), nullable=False)
	password = db.Column(db.String(128), nullable=False)

	def __init__(self, login, password):
		self.login = login
		self.password = password

	def hash_password(self, password):
		self.password = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password)


class Acesso(db.Model, CRUD):
	__tablename__ = "acesso"

	id = db.Column(db.Integer, primary_key=True)
	id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
	nome_sala = db.Column(db.String(4), db.ForeignKey('sala.nome'), nullable=False)
	sync = db.Column(db.Boolean, nullable=False)
	salas = db.relationship('Sala')
	usuario = db.relationship('Usuario', uselist=False)

	def __init__(self, sync, salas, usuario):
		self.sync = sync
		self.salas = salas
		self.usuario = usuario


class Horario(db.Model, CRUD):
	__tablename__ = "horario"

	id = db.Column(db.Integer, primary_key=True)
	hora_inicio = db.Column(db.DateTime, nullable=False)
	hora_fim = db.Column(db.DateTime, nullable=False)
	dia = db.Column(db.String(15), nullable=False)
	tipo_user = db.Column(db.String(15), nullable=False)
	sync = db.Column(db.Boolean, nullable=False)
	nome_sala = db.Column(db.String(4), db.ForeignKey('sala.nome'), nullable=False)

	def __init__(self, nome_sala, hora_fim, hora_inicio, dia, tipo_user, sync):
		self.nome_sala = nome_sala
		self.hora_fim = hora_fim
		self.hora_inicio = hora_inicio
		self.dia = dia
		self.tipo_user = tipo_user
		self.sync = sync


class Relatorio(db.Model, CRUD):
	__tablename__ = "relatorio"

	id = db.Column(db.Integer, primary_key=True)
	tipo_in_out = db.Column(db.String(1), nullable=False)
	horario = db.Column(db.DateTime, nullable=False)
	acesso_nome_sala = db.Column(db.String(4), db.ForeignKey('acesso.nome_sala'))
	acesso_id_usuario = db.Column(db.Integer, db.ForeignKey('acesso.id_usuario'))

	def __init__(self, tipo_in_out, horario):
		self.tipo_in_out = tipo_in_out
		self.horario = horario


class Sala(db.Model, CRUD):
	__tablename__ = "sala"

	nome = db.Column(db.String(4), primary_key=True)
	horarios = db.relationship('Horario')

	def __init__(self, nome):
		self.nome = nome


class Usuario(db.Model, CRUD):
	__tablename__ = "usuario"

	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String(80), nullable=False)
	email = db.Column(db.String(100), nullable=False)
	rfid = db.Column(db.String(16), nullable=False)

	def __init__(self, nome, email, rfid):
		self.nome = nome
		self.email = email
		self.rfid = rfid
