from flask import jsonify
from flask_restful import Resource, reqparse
import dateutil.parser
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

from setup import db
from evento_model import Evento, EventoSchema
from sala_model import Sala, SalaSchema
from usuario_model import Usuario, UsuarioSchema

schema = EventoSchema()
schema2 = SalaSchema()
schema3 = UsuarioSchema()

class RaspEventoResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("rfid", type=str, required=True, location="json")
        parser.add_argument("evento", type=str, required=True, location="json")
        parser.add_argument("horario", type=str, required=True, location="json")
        parser.add_argument("sala", type=str, required=True, location="json")
        args = parser.parse_args(strict=True)
        
        sala_query = Sala.query.filter(Sala.nome == args["sala"]).first()
        sala = schema2.dump(sala_query).data
        id_sala = sala["id"]

        usuario_query = Usuario.query.filter(Usuario.rfid == args["rfid"]).first()
        usuario = schema3.dump(usuario_query).data
        id_usuario = usuario["id"]
        
        try:
            evento = Evento(args["evento"], dateutil.parser.parse(args["horario"]), id_usuario, id_sala)
            evento.add(evento)
            query = Evento.query.get(evento.id)
        except SQLAlchemyError as e:
            db.session.rollback()
            response = jsonify({"message": str(e)})
            response.status_code = 403
            return response
        else:
            return schema.dump(query).data, 201
        