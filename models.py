from passlib.apps import custom_app_context as pwd_context

from base import CRUD, db


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
