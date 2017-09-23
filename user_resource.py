from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Resource, reqparse

from setup import db
from acesso_model import Acesso
from user_model import Usuario, UsuarioSchema

schema = UsuarioSchema()


class UsuarioResource(Resource):
	def get(self, id):
		user_query = Usuario.query.get(id)
		result = schema.dump(user_query).data
		return result

	# OLHAR QUERY PARAMETERS \\ FUNCIONANDO APENAS PARA EDITAR NOME
	def put(self, id):
		parser = reqparse.RequestParser()

		parser.add_argument("nome", type=str, location='json')
		parser.add_argument("email", type=str, location='json')
		parser.add_argument("salas", action='append', location='json')

		args = parser.parse_args(strict=True)
		user = Usuario.query.get(id)

		if args["nome"] and user.nome != args["nome"]:
			user.nome = args["nome"]

		if args["email"] and user.email != args["email"]:
			user.email = args["email"]

		# CASO NÃO TENHAM SALAS NO JSON E TENHAM NO BANCO, RETIRAR O ACESSO DE TODAS AS SALAS
		# banco: ["E100", "E007", "E003"]
		# json:  []
		if not args["salas"] and user.acessos:
			try:
				for acesso in user.acessos:
					acesso = Acesso(id, acesso.nome_sala)
					db.session.query(Acesso).\
						filter(Acesso.id_usuario == id,
								Acesso.nome_sala == acesso.nome_sala)\
						.delete(synchronize_session='evaluate')
			except SQLAlchemyError as e:
				db.session.rollback()
				resp = jsonify({"error": str(e)})
				resp.status_code = 403
				return resp

		# CASO HAJAM SALAS NO JSON E NO BANCO
		elif args["salas"]:
			acessos = [acesso.nome_sala for acesso in user.acessos]
			to_add = [sala for sala in args["salas"] if sala not in acessos]
			to_remove = [sala for sala in acessos if sala not in args["salas"]]

			# NOVO ACESSO
			if to_add:
				try:
					for sala in to_add:
						acesso = Acesso(id, sala)
						acesso.add(acesso)
				except SQLAlchemyError as e:
					db.session.rollback()
					resp = jsonify({"error": str(e)})
					resp.status_code = 403
					return resp

			# REMOVER ACESSO
			if to_remove:
				try:
					for sala in to_remove:
						acesso = Acesso(id, sala)
						db.session.query(Acesso).\
							filter(Acesso.id_usuario == id,
								Acesso.nome_sala == sala)\
							.delete(synchronize_session='evaluate')
				except SQLAlchemyError as e:
					db.session.rollback()
					resp = jsonify({"error": str(e)})
					resp.status_code = 403
					return resp

		db.session.commit()
		return schema.dump(user).data

	def delete(self, id):
		try:
			user = Usuario.query.get(id)
			if not user:
				response = jsonify({"message": "Usuario {} doesn't exist".format(id)})
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
	def get(self):
		users_query = Usuario.query.all()
		results = schema.dump(users_query, many=True).data
		return results

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument("nome", type=str, required=True, location='json')
		parser.add_argument("email", type=str, required=True, location='json')
		parser.add_argument("rfid", type=str, required=True, location='json')

		parser.add_argument("salas", action='append', location='json')
		args = parser.parse_args(strict=True)

		try:
			user = Usuario(args["nome"], args["email"], args["rfid"])
			user.add(user)
			if args["salas"]:
				try:
					for sala in args["salas"]:
						acesso = Acesso(user.id, sala)
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
			return schema.dump(query).data, 201, {'location': 'api/v1/users/' + str(user.id)}
