from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Resource, reqparse

from setup import db
from sala_model import Sala, SalaSchema

schema = SalaSchema()


class SalaResource(Resource):
	def get(self, nome):
		sala_query = Sala.query.get(nome)
		result = schema.dump(sala_query).data
		return result

	def put(self, nome):
		pass  # TO DO

	def delete(self, nome):
		try:
			sala = Sala.query.get(nome)
			if not sala:
				response = jsonify({"message": "Sala {} doesn't exist".format(nome)})
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
	def get(self):
		salas = Sala.query.all()
		results = schema.dump(salas, many=True).data
		return results

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument("nome", type=str, required=True, location='json')

		args = parser.parse_args(strict=True)
		try:

			sala = Sala(args["nome"])
			sala.add(sala)
			query = Sala.query.get(sala.nome)

		except SQLAlchemyError as e:
			db.session.rollback()
			resp = jsonify({"error": str(e)})
			resp.status_code = 403
			return resp
		else:
			return schema.dump(query).data, 201, {'location': '/salas/' + sala.nome}
