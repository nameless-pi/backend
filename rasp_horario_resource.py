from flask import jsonify
from flask_restful import Resource, reqparse
import dateutil.parser

from setup import db
from horario_model import Horario, HorarioSchema
from sala_model import Sala, SalaSchema

schema = HorarioSchema()
schema2 = SalaSchema()

class RaspHorarioResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("last_update", type=str, required=True, location="json")
        parser.add_argument("sala", type=str, required=True, location="json")
        args = parser.parse_args(strict=True)

        sala = args["sala"]
        hora = dateutil.parser.parse(args["last_update"])
        print(hora)

        sala_query = Sala.query.all()
        salas = schema2.dump(sala_query, many=True).data
        for s in salas:
            if s["nome"] == sala:
                id_sala = s["id"]
                print(id_sala)
        print(id_sala)
        
        
        horario_query = Horario.query.all()
        horarios = schema.dump(horario_query, many=True).data
        print(horarios)
        results = []
        for h in horarios:
            if (h["id_sala"] == id_sala) and (dateutil.parser.parse(h["last_update"]) > hora):
                adicionar = {}
                adicionar.update({"dia":h["dia"]})
                adicionar.update({"hora_inicio":h["hora_inicio"]})
                adicionar.update({"hora_fim":h["hora_fim"]})
                adicionar.update({"tipo_usuario":h["tipo_user"]})
                adicionar.update({"last_update":h["last_update"]})
                results.append(adicionar)
                adicionar = {}
        print("\n")
        print(results)
        print("\n")
        
        return jsonify(results)