from flask import jsonify
from flask_jwt import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Resource, reqparse

from setup import db
from sala_model import Sala, SalaSchema

schema = SalaSchema()


class SalaResource(Resource):
	# @jwt_required()
	def get(self, id):
		sala_query = Sala.query.get(id)
		if not sala_query:
			response = jsonify({"message": "Sala {} doesn't exist".format(id)})
			response.status_code = 404
			return response
		return schema.dump(sala_query).data

	# @jwt_required()
	def put(self, id):
		parser = reqparse.RequestParser()
		parser.add_argument("nome", type=str, required=True, location='json')

		args = parser.parse_args(strict=True)
		sala = Sala.query.get(id)

		if sala.nome != args["nome"]:
			sala.nome = args["nome"]

		try:
			sala.update()
		except SQLAlchemyError as e:
			db.session.rollback()
			resp = jsonify({"error": str(e)})
			resp.status_code = 403
			return resp
		else:
			return schema.dump(sala).data

	# @jwt_required()
	def delete(self, id):
		try:
			sala = Sala.query.get(id)
			if not sala:
				response = jsonify({"message": "Sala {} doesn't exist".format(id)})
				response.status_code = 404
				return response
			sala.delete(sala)
		except SQLAlchemyError as e:
			db.session.rollback()
			resp = jsonify({"error": str(e)})
			resp.status_code = 403
			return resp
		else:
			return None, 204


class SalaListResource(Resource):
	# @jwt_required()
	def get(self):
		salas = Sala.query.all()
		results = schema.dump(salas, many=True).data
		return results

	# @jwt_required()
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument("nome", type=str, required=True, location='json')

		args = parser.parse_args(strict=True)
		try:
			sala = Sala(args["nome"])
			sala.add(sala)
			query = Sala.query.order_by(Sala.id.desc()).first()

		except SQLAlchemyError as e:
			db.session.rollback()
			resp = jsonify({"error": str(e)})
			resp.status_code = 403
			return resp
		else:
			return schema.dump(query).data, 201, {'location': 'api/v1/salas/' + str(query.id)}
