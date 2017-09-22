from setup import api, app
from user_resource import UsuarioResource, UsuarioListResource
from sala_resource import SalaResource, SalaListResource
from horario_resource import HorarioResource, HorarioListResource


api.add_resource(UsuarioResource, "/api/v1/users/<int:id>")
api.add_resource(UsuarioListResource, "/api/v1/users")

api.add_resource(SalaResource, "/api/v1/salas/<string:nome>")
api.add_resource(SalaListResource, "/api/v1/salas")

api.add_resource(HorarioResource, "/api/v1/horarios/<int:id>")
api.add_resource(HorarioListResource, "/api/v1/horarios")

if __name__ == '__main__':
	app.run(host=app.config['HOST'],
			port=app.config['PORT'],
			debug=app.config['DEBUG'])
