from flask import jsonify
from flask_restful import Resource, reqparse
import dateutil.parser
from sqlalchemy import desc

from setup import db
from evento_model import Evento, EventoSchema
from sala_model import Sala, SalaSchema

schema = EventoSchema()
schema2 = SalaSchema()

class RaspCheckEventoResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("sala", type=str, required=True, location="json")
        args = parser.parse_args(strict=True)

        sala = args["sala"]

        sala_query = Sala.query.filter(Sala.nome == sala).first()
        salas = schema2.dump(sala_query).data
        id_sala = salas["id"]        

        evento_query = Evento.query.filter(Evento.id_sala == id_sala).order_by(desc(Evento.horario)).first()
        eventos = schema.dump(evento_query).data
        results = {}
        if eventos == {}:
            results.update({"horario": "2001-01-01T00:00:00+00:00"})
        else:
            results.update({"horario": eventos["horario"]})
        
        return jsonify(results)