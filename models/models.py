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
	__tablename__ = 'admins'

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


class Usuario(db.Model, CRUD):
	__tablename__ = "usuario"

	id = db.Column(db.Integer, primary_key=True)
	rfid = db.Column(db.String(16), nullable=False,unique=True)
	nome = db.Column(db.String(80), nullable=False)
	email = db.Column(db.String(100), nullable=False,unique=True)
	acessos = db.relationship('Acesso')

	def __init__(self, rfid, nome, email):
		self.rfid = rfid
		self.nome = nome
		self.email = email



class Horario(db.Model, CRUD):
	__tablename__ = "horario"
	id = db.Column(db.Integer, primary_key=True)
	hora_inicio = db.Column(db.DateTime, nullable=False)
	hora_fim = db.Column(db.DateTime, nullable=False)
	dia = db.Column(db.String(15), nullable=False)
	tipo_user = db.Column(db.String(15), nullable=False)
	sync = db.Column(db.Boolean, nullable=False)
	nome_sala = db.Column(db.String(4), db.ForeignKey('sala.nome'),nullable = False)   

	def __init__(self, hora_fim, hora_inicio, dia, tipo_user, sync):
		self.hora_fim = hora_fim
		self.hora_inicio = hora_inicio
		self.dia = dia
		self.tipo_user = tipo_user
		self.sync = sync




class Sala(db.Model, CRUD):
	__tablename__ = "sala"

	nome = db.Column(db.String(4), primary_key=True)
	horarios = db.relationship('Horario')

	def __init__(self, nome, horarios):
		self.nome = nome
		self.horarios = horarios


class Acesso(db.Model, CRUD):
	__tablename__ = "acesso"

	id = db.Column(db.Integer, primary_key=True)
	id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'),  nullable=False)
	nome_sala = db.Column(db.String(4), db.ForeignKey('sala.nome'), nullable=False)
	sync = db.Column(db.Boolean, nullable=False)
	salas = db.relationship('Sala')
	

	def __init__(self, sync, salas):
		self.sync = sync
		self.salas = salas
	


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
