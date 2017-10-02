from ast import literal_eval
from flask import jsonify
from flask_jwt import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Resource, reqparse

from setup import db
from acesso_model import DireitoAcesso
from user_model import Usuario, UsuarioSchema

schema = UsuarioSchema()


class UsuarioResource(Resource):
	@jwt_required()
	def get(self, id):
		user_query = Usuario.query.get(id)
		if not user_query:
			response = jsonify({"message": "Usuario {} não existe".format(id)})
			response.status_code = 404
			return response
		return schema.dump(user_query).data

	@jwt_required()
	def put(self, id):
		parser = reqparse.RequestParser()

		parser.add_argument("nome", type=str, location="json")
		parser.add_argument("rfid", type=str, location="json")
		parser.add_argument("tipo", type=str, location="json")
		parser.add_argument("email", type=str, location="json")
		parser.add_argument("direito_acesso", action="append", location="json")

		args = parser.parse_args(strict=True)
		user = Usuario.query.get(id)

		if not user:
			response = jsonify({"message": "Usuario {} não existe".format(id)})
			response.status_code = 404
			return response

		if args["rfid"] and user.rfid != args["rfid"]:
			if db.session.query(Usuario).filter(Usuario.rfid == args["rfid"]).all():
				response = jsonify({"message": "RFID existente"})
				response.status_code = 403
				return response
			else:
				user.rfid = args["rfid"]

		if args["nome"] and user.nome != args["nome"]:
			user.nome = args["nome"]

		if args["email"] and user.email != args["email"]:
			if db.session.query(Usuario).filter(Usuario.email == args["email"]).all():
				response = jsonify({"message": "Email existente"})
				response.status_code = 403
				return response
			else:
				user.email = args["email"]

		if args["tipo"] and user.tipo != args["tipo"]:
			user.tipo = args["tipo"]


		# CASO NÃO TENHAM SALAS NO JSON E TENHAM NO BANCO, RETIRAR O ACESSO DE TODAS AS SALAS
		# banco: [{"id_sala": 1, "nome_sala": "E001"}]
		# json:  []
		if not args["direito_acesso"] and user.direito_acesso:
			try:
				for acesso in user.direito_acesso:
					db.session.query(DireitoAcesso)\
						.filter(DireitoAcesso.id_usuario == id,
							DireitoAcesso.id_sala == acesso.id_sala)\
						.delete(synchronize_session="evaluate")
			except SQLAlchemyError as e:
				db.session.rollback()
				resp = jsonify({"error": str(e)})
				resp.status_code = 403
				return resp

		# CASO HAJAM SALAS NO JSON E NO BANCO
		# [{"id": 1, "nome": "E001"}]
		elif args["direito_acesso"]:
			"""
				args -> contém os IDs das salas passadas no JSON
				acessos -> contém os IDs das salas do banco
			"""
			args = [literal_eval(i)["id_sala"] for i in args["direito_acesso"]]
			acessos = [acesso.id_sala for acesso in user.direito_acesso] #  acessos do usuário
			to_add = [id_sala for id_sala in args if id_sala not in acessos]
			to_remove = [id_sala for id_sala in acessos if id_sala not in args]

			# NOVO ACESSO
			if to_add:
				try:
					for id_sala in to_add:
						acesso = DireitoAcesso(id, id_sala)
						acesso.add(acesso)
				except SQLAlchemyError as e:
					db.session.rollback()
					resp = jsonify({"error": str(e)})
					resp.status_code = 403
					return resp

			# REMOVER ACESSO
			if to_remove:
				try:
					for id_sala in to_remove:
						acesso = DireitoAcesso(id, id_sala)
						db.session.query(DireitoAcesso).\
							filter(DireitoAcesso.id_usuario == id,
								DireitoAcesso.id_sala == id_sala)\
							.delete(synchronize_session="evaluate")
				except SQLAlchemyError as e:
					db.session.rollback()
					resp = jsonify({"error": str(e)})
					resp.status_code = 403
					return resp
		user.update()
		return schema.dump(user).data

	@jwt_required()
	def delete(self, id):
		try:
			user = Usuario.query.get(id)
			if not user:
				response = jsonify({"message": "Usuario {} não existe".format(id)})
				response.status_code = 404
				return response
			user.delete(user)
		except SQLAlchemyError as e:
			db.session.rollback()
			resp = jsonify({"error": str(e)})
			resp.status_code = 403
			return resp
		else:
			return None, 204


class UsuarioListResource(Resource):
	@jwt_required()
	def get(self):
		users_query = Usuario.query.all()
		results = schema.dump(users_query, many=True).data
		return results

	@jwt_required()
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument("nome", type=str, required=True, location="json")
		parser.add_argument("rfid", type=str, required=True, location="json")
		parser.add_argument("tipo", type=str, required=True, location="json")
		parser.add_argument("email", type=str, required=True, location="json")

		parser.add_argument("direito_acesso", action="append", location="json")
		args = parser.parse_args(strict=True)

		try:
			user = Usuario(args["nome"], args["email"], args["rfid"], args["tipo"])
			user.add(user)
			if args["direito_acesso"]:
				try:
					for sala in args["direito_acesso"]:
						# [{"id": 1, "nome": "E001"}]
						sala = literal_eval(sala)
						acesso = DireitoAcesso(user.id, sala["id"])
						acesso.add(acesso)
				except SQLAlchemyError as e:
					db.session.rollback()
					resp = jsonify({"error": str(e)})
					resp.status_code = 403
					return resp
			query = Usuario.query.get(user.id)

		except SQLAlchemyError as e:
			db.session.rollback()
			resp = jsonify({"error": str(e)})
			resp.status_code = 403
			return resp
		else:
			# 				JSON 		status_code		location
			return schema.dump(query).data, 201, {"location": "api/v1/users/" + str(user.id)}
