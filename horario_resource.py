from flask import jsonify
from flask_jwt import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Resource, reqparse

from setup import db
from horario_model import Horario, HorarioSchema

schema = HorarioSchema()


class HorarioResource(Resource):
	@jwt_required()
	def get(self, id):
		horario_query = Horario.query.get(id)
		result = schema.dump(horario_query).data
		return result

	@jwt_required()
	def put(self, id):
		parser = reqparse.RequestParser()

		parser.add_argument("nome_sala", type=str, location='json')
		parser.add_argument("hora_inicio", type=str, location='json')
		parser.add_argument("hora_fim", type=str, location='json')
		parser.add_argument("dia", type=str, location='json')
		parser.add_argument("tipo_user", type=str, location='json')
		parser.add_argument("sync", type=str, location='json')

		args = parser.parse_args(strict=True)
		horario = Horario.query.get(id)

		if args["nome_sala"] and args["nome_sala"] != horario.nome_sala:
			horario.nome_sala = args["nome_sala"]

		if args["hora_inicio"] and args["hora_inicio"] != horario.hora_inicio:
			horario.hora_inicio = args["hora_inicio"]

		if args["hora_fim"] and args["hora_fim"] != horario.hora_fim:
			horario.hora_fim = args["hora_fim"]

		if args["dia"] and args["dia"] != horario.dia:
			horario.dia = args["dia"]

		if args["tipo_user"] and args["tipo_user"] != horario.tipo_user:
			horario.tipo_user = args["tipo_user"]

		if args["sync"] and args["sync"] != horario.sync:
			horario.sync = args["sync"]

		horario.update()
		return schema.dump(horario).data

	@jwt_required()
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
	@jwt_required()
	def get(self):
		horarios_query = Horario.query.all()
		results = schema.dump(horarios_query, many=True).data
		return results

	@jwt_required()
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
			return schema.dump(query).data, 201, {'location': 'api/v1/horarios/' + str(horario.id)}
