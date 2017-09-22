from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Resource, reqparse

from setup import db
from horario_model import Horario, HorarioSchema

schema = HorarioSchema()


class HorarioResource(Resource):
	def get(self, id):
		horario_query = Horario.query.get(id)
		result = schema.dump(horario_query).data
		return result

	def put(self, id):
		pass  # TO DO

	def delete(self, id):
		try:
			horario = Horario.query.get(id)
			if not horario:
				response = jsonify({"message": "Horario {} doesn't exist".format(id)})
				response.status_code = 404
				return response
			horario.delete(horario)
		except SQLAlchemyError as e:
			db.session.rollback()
			resp = jsonify({"error": str(e)})
			resp.status_code = 403
			return resp
		else:
			return None, 204


class HorarioListResource(Resource):
	def get(self):
		horarios_query = Horario.query.all()
		results = schema.dump(horarios_query, many=True).data
		return results

	def post(self):
		parser = reqparse.RequestParser()

		parser.add_argument("nome_sala", type=str, required=True, location='json')
		parser.add_argument("hora_inicio", type=str, required=True, location='json')
		parser.add_argument("hora_fim", type=str, required=True, location='json')
		parser.add_argument("dia", type=str, required=True, location='json')
		parser.add_argument("tipo_user", type=str, required=True, location='json')
		parser.add_argument("sync", type=str, required=True, location='json')

		args = parser.parse_args(strict=True)
		try:
			horario = Horario(args["nome_sala"], args["hora_inicio"], args["hora_fim"],
							args["dia"], args["tipo_user"], args["sync"])
			horario.add(horario)
			query = Horario.query.get(horario.id)

		except SQLAlchemyError as e:
			db.session.rollback()
			resp = jsonify({"error": str(e)})
			resp.status_code = 403
			return resp
		else:
			return schema.dump(query).data, 201, {'location': '/horarios/' + str(horario.id)}
