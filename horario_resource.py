from flask import jsonify
from flask_jwt import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Resource, reqparse

from datetime import datetime

from setup import db
from horario_model import Horario, HorarioSchema

schema = HorarioSchema()


class HorarioResource(Resource):
	@jwt_required()
	def get(self, id):
		horario_query = Horario.query.get(id)
		if  horario_query.alive == False:
			response = jsonify({"message": "Horario {} não existe".format(id)})
			response.status_code = 404
			return response
		result = schema.dump(horario_query).data
		return result

	@jwt_required()
	def put(self, id):
		parser = reqparse.RequestParser()

		parser.add_argument("hora_inicio", type=str, location="json")
		parser.add_argument("hora_fim", type=str, location="json")
		parser.add_argument("dia", type=str, location="json")
		parser.add_argument("tipo_user", type=str, location="json")
		parser.add_argument("id_sala", type=str, location="json")

		args = parser.parse_args(strict=True)
		horario = Horario.query.get(id)

		if horario.alive == False:
			response = jsonify({"message": "Horario {} não existe".format(id)})
			response.status_code = 404
			return response

		horario_check = db.session.query(Horario)\
			.filter(Horario.id_sala == args["id_sala"],
					Horario.dia == args["dia"],
					Horario.tipo_user == args["tipo_user"],
					Horario.hora_inicio == args["hora_inicio"],
					Horario.hora_fim == args["hora_fim"]).all()

		if horario_check:
			response = jsonify({"message": "Horário existente"})
			response.status_code = 403
			return response

		if args["hora_inicio"] and args["hora_inicio"] != horario.hora_inicio:
			horario.hora_inicio = args["hora_inicio"]

		if args["hora_fim"] and args["hora_fim"] != horario.hora_fim:
			horario.hora_fim = args["hora_fim"]

		if args["dia"] and args["dia"] != horario.dia:
			horario.dia = args["dia"]

		if args["tipo_user"] and args["tipo_user"] != horario.tipo_user:
			horario.tipo_user = args["tipo_user"]

		horario.last_update = datetime.now()
		horario.update()
		return schema.dump(horario).data

	@jwt_required()
	def delete(self, id):
		try:
			horario = Horario.query.get(id)
			if horario.alive == False:
				response = jsonify({"message": "Horario {} não existe".format(id)})
				response.status_code = 404
				return response
			horario.alive = False
			horario.last_update = datetime.now()
			horario.update()
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
		horarios_query = Horario.query.filter(Horario.alive == True).all()
		return schema.dump(horarios_query, many=True).data
	
	@jwt_required()
	def get_by_sala(self,id):
	   	horarios = Horario.query.filter(Horario.alive == True, Horario.id_sala == id).all()
	   	return schema.dump(horarios,many=True).data
	
	def get_by_sala_and_day(self,id_sala,day):
		horarios = Horario.query.filter(Horario.alive == True, 
										Horario.id_sala == id_sala, 
										Horario.dia == day).all()
		return schema.dump(horarios,many=True).data

	@jwt_required()
	def post(self):
		parser = reqparse.RequestParser()

		parser.add_argument("id_sala", type=int, required=True, location="json")
		parser.add_argument("hora_inicio", type=str, required=True, location="json")
		parser.add_argument("hora_fim", type=str, required=True, location="json")
		parser.add_argument("dia", type=str, required=True, location="json")
		parser.add_argument("tipo_user", type=str, required=True, location="json")

		args = parser.parse_args(strict=True)

		horario_check = db.session.query(Horario)\
			.filter(Horario.id_sala == args["id_sala"],
					Horario.dia == args["dia"],
					Horario.tipo_user == args["tipo_user"],
					Horario.hora_inicio == args["hora_inicio"],
					Horario.hora_fim == args["hora_fim"]).all()

		if horario_check and not horario_check[0].alive:
			query = Horario.query.get(horario_check[0].id)
			query.alive = True
			query.last_update = datetime.now()
			query.update()
			return schema.dump(query).data, 201, {"location": "api/v1/horarios/" + str(query.id)}
		elif horario_check:
			resp = jsonify({"message": "Este horário já existe"})
			resp.status_code = 403
			return resp

		try:			
			horario = Horario(args["id_sala"], args["dia"], 
				args["hora_inicio"], args["hora_fim"],
				args["tipo_user"])
			horario.add(horario)
			query = Horario.query.get(horario.id)

		except SQLAlchemyError as e:
			db.session.rollback()
			resp = jsonify({"error": str(e)})
			resp.status_code = 403
			return resp
		else:
			return schema.dump(query).data, 201, {"location": "api/v1/horarios/" + str(horario.id)}
