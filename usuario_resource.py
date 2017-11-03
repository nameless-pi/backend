from ast import literal_eval
from flask import jsonify
from flask_jwt import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Resource, reqparse

from datetime import datetime

from setup import db
from acesso_model import DireitoAcesso
from usuario_model import Usuario, UsuarioSchema

schema = UsuarioSchema()


class UsuarioResource(Resource):
	@jwt_required()
	def get(self, id):
		user_query = Usuario.query.get(id)
		if user_query.alive == False:
			response = jsonify({"message": "Usuario {} não existe".format(id)})
			response.status_code = 404
			return respons
		direitos_de_acesso = DireitoAcesso.query.filter(DireitoAcesso.alive == True,DireitoAcesso.id_usuario == id).all()
		user = [{"id":getattr("id"),"nome":getattr("nome"),"tipo":getattr("tipo"),"email":getattr("email"),"rfid":getattr("rfid"),
	   			"direito_acesso":direitos_de_acesso,"last_update":getattr("last_update"),"alive":getattr("alive")}]
		return schema.dump(user).data

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

		if user.alive == False:
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

		# CASO NÃO TENHAM SALAS NO JSON, RETIRAR O ACESSO DE TODAS AS SALAS
		if not args["direito_acesso"]:
			
				for acesso in user.direito_acesso:
	   				acesso.alive = False;

		# CASO HAJAM SALAS NO JSON E NO BANCO
		# [{"id": 1, "nome": "E001"}]
		elif args["direito_acesso"]:

			args = [literal_eval(i)["id_sala"] for i in args["direito_acesso"]]  # id do JSON
			acessos = [acesso.id_sala for acesso in user.direito_acesso]  # id do usuário
			to_add = [i for i in args if i not in acessos] # tá no JSON, mas não no BANCO

			for acesso in user.direito_acesso:
    				
				if acesso.id_sala in args and not acesso.alive:  # sala tá no JSON e BANCO, mas tá morto no banco
					acesso.alive = True
				elif acesso.id_sala not in args and acesso.alive: # sala não tá no JSON e está no BANCO como vivo
					acesso.alive = False

			for new_acesso in to_add:
				acesso = DireitoAcesso(id, new_acesso)
				acesso.add(acesso)

		user.last_update = datetime.now()
		user.update()
		return schema.dump(user).data

	@jwt_required()
	def delete(self, id):
		try:
			user = Usuario.query.get(id)
			if user.alive == False:
				response = jsonify({"message": "Usuario {} não existe".format(id)})
				response.status_code = 404
				return response
			user.alive = False
			for acesso in user.direito_acesso:
	   			acesso.alive = False
			user.last_update = datetime.now()
			user.update()
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
		users_query = Usuario.query.filter(Usuario.alive == True).all()
		
		usuarios = [{"id":getattr(i,"id"),"nome":getattr(i,"nome"),"tipo":getattr(i,"tipo"),"email":getattr(i,"email"),"rfid":getattr(i,"rfid"),
	   			"direito_acesso":getattr(i,"direito_acesso"),"last_update":getattr(i,"last_update"),"alive":getattr(i,"alive")} for i in users_query]
		for usuario in usuarios:
	   		usuario["direito_acesso"] = DireitoAcesso.query.filter(DireitoAcesso.alive == True, DireitoAcesso.id_usuario == usuario["id"]).all()
		results = schema.dump(usuarios, many=True).data
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
						acesso = DireitoAcesso(user.id, sala["id_sala"])
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
			return schema.dump(query).data, 201, {"location": "api/v1/usuarios/" + str(user.id)}

	@jwt_required()
	def delete(self):
		'''
			Como não é removido o usuário, não há necessidade de
			remover os direito_acesso primeiro, logo é só setado como False as flags de acessos do usuário
		'''
		try:
			usuarios = Usuario.query.all()
			for usuario in usuarios:
				usuario.alive = False
				for acesso in user.direito_acesso:
	   	   			acesso.alive = False
				Usuario.last_update = datetime.now()
				Usuario.update()
		except SQLAlchemyError as e:
			db.session.rollback()
			resp = jsonify({"error": str(e)})
			resp.status_code = 403
			return resp
		else:
			return None, 204
