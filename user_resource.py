from flask import jsonify
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

		parser.add_argument("nome", type=str, required=True, location='json')
		args = parser.parse_args(strict=True)

		user = Usuario.query.get(id)
		user.nome = args.get("nome")
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

		parser.add_argument("salas", action='append', required=True, location='json')
		args = parser.parse_args(strict=True)

		try:
			user = Usuario(args["nome"], args["email"], args["rfid"])
			user.add(user)

			for sala in args["salas"]:
				acesso = Acesso(user.id, sala)
				acesso.add(acesso)

			query = Usuario.query.get(user.id)

		except SQLAlchemyError as e:
			db.session.rollback()
			resp = jsonify({"error": str(e)})
			resp.status_code = 403
			return resp
		else:
			# 				JSON 		status_code		location
			return schema.dump(query).data, 201, {'location': '/users/' + str(user.id)}
