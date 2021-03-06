from flask import jsonify
from flask_jwt import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Resource, reqparse

from datetime import datetime

from setup import db
from sala_model import Sala, SalaSchema
from horario_model import Horario
from acesso_model import DireitoAcesso
from usuario_model import Usuario

schema = SalaSchema()


class SalaHorarioResource(Resource):
	@jwt_required()
	def delete(self, id):
		try:
			horarios = [i[0] for i in db.session.query(Horario).filter(Horario.id_sala == id).all()]
			for horario in horarios:
				horario.alive = False
				horario.last_update = datetime.now()
				horario.commit()
		except SQLAlchemyError as e:
			db.session.rollback()
			resp = jsonify({"error": str(e)})
			resp.status_code = 403
			return resp
		else:
			return None, 204


class SalaResource(Resource):
	@jwt_required()
	def get(self, id):
		sala_query = Sala.query.get(id)
		
		if sala_query.alive == False:
			response = jsonify({"message": "Sala {} não existe".format(id)})
			response.status_code = 404
			return response
		return schema.dump(sala_query).data

	@jwt_required()
	def put(self, id):
		parser = reqparse.RequestParser()
		parser.add_argument("nome", type=str, required=True, location="json")

		args = parser.parse_args(strict=True)
		sala = Sala.query.get(id)

		if sala.alive == False:
			response = jsonify({"message": "Sala {} não existe".format(id)})
			response.status_code = 404
			return response

		if sala.nome != args["nome"]:
			sala.nome = args["nome"]

		try:
			sala.last_update = datetime.now()
			sala.update()
		except SQLAlchemyError as e:
			db.session.rollback()
			resp = jsonify({"error": str(e)})
			resp.status_code = 403
			return resp
		else:
			return schema.dump(sala).data

	@jwt_required()
	def delete(self, id):
		try:
			sala = Sala.query.get(id)
			if sala.alive == False:
				response = jsonify({"message": "Sala {} não existe".format(id)})
				response.status_code = 404
				return response
			sala.alive = False
			acessos = db.session.query(DireitoAcesso).filter(DireitoAcesso.id_sala == id).all()
			for acesso in acessos:
				acesso.alive = False
			sala.last_update = datetime.now()
			sala.update()
		except SQLAlchemyError as e:
			db.session.rollback()
			resp = jsonify({"error": str(e)})
			resp.status_code = 403
			return resp
		else:
			return None, 204


class SalaListResource(Resource):
	@jwt_required()
	def get(self):
		salas = Sala.query.filter(Sala.alive == True).all()

		salas = [{	"id": getattr(i, "id"), 
					"nome": getattr(i, "nome"), 
					"horarios": getattr(i, "horarios")
				} for i in salas]
				
		for sala in salas:
			sala["horarios"] = Horario.query.filter(Horario.alive == True, 
													Horario.id_sala == sala["id"]).all()
		results = schema.dump(salas, many=True).data
		return results

	
	@jwt_required()
	def get_sala_by_user(self,id_user):
		acessos = db.session.query(Usuario.direito_acesso).filter(
													Usuario.alive == True,
													Usuario.id == id_user
													).all()
		salas = []
		for acesso in acessos:
			sala = Sala.query.get(acesso.id_sala)
			if sala.alive:
				salas.append(sala)

		salas_alive = [{	"id": getattr(i, "id"), 
					"nome": getattr(i, "nome"), 
					"horarios": getattr(i, "horarios")
				} for i in salas]
				
		for sala in salas_alive:
			sala["horarios"] = Horario.query.filter(Horario.alive == True, 
													Horario.id_sala == sala["id"]).all()
		 
		return schema.dump(salas_alive, many=True).data

	@jwt_required()
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument("nome", type=str, required=True, location="json")
		args = parser.parse_args(strict=True)
		sala_nova_id = db.session.query(Sala.id).filter(Sala.alive == False, 
														Sala.nome == args["nome"]).all()
		
		if sala_nova_id:
			sala_nova = Sala.query.get(sala_nova_id[0][0])
			sala_nova.alive = True
			sala_nova.last_update = datetime.now()
			sala_nova.update()
			salas = {	"id": getattr(sala_nova, "id"), 
						"nome": getattr(sala_nova, "nome"), 
						"horarios":[],
						"last_update": getattr(sala_nova,"last_update"),
						"alive": getattr(sala_nova,"alive")
				}
			
			return schema.dump(salas).data, 201, {"location": "api/v1/salas/" + str(salas["id"])}
		else:
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
				return schema.dump(query).data, 201, {"location": "api/v1/salas/" + str(query.id)}

	@jwt_required()
	def delete(self):
		try:
			salas = Sala.query.all()
			for sala in salas:
	   			sala.alive = False
	   			sala.last_update = datetime.now()
	   			sala.update()
		except SQLAlchemyError as e:
			db.session.rollback()
			resp = jsonify({"error": str(e)})
			resp.status_code = 403
			return resp
		else:
			return None, 204
