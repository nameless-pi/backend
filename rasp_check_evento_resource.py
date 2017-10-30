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

        sala_query = Sala.query.all()
        salas = schema2.dump(sala_query, many=True).data
        for s in salas:
            if s["nome"] == sala:
                id_sala = s["id"]
        
        

        evento_query = Evento.query.filter(Evento.id_sala == id_sala).order_by(desc(Evento.horario)).first()
        eventos = schema.dump(evento_query).data
        results = []
        if eventos == {}:
            results.append({"horario": "2001-01-01T00:00:00+00:00"})
        else:
            results.append({"horario": eventos["horario"]})
        
        print(results)
        return (results)