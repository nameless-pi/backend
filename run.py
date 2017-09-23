from setup import api, app
from admin_resource import AdminResource
from sala_resource import SalaResource, SalaListResource
from user_resource import UsuarioResource, UsuarioListResource
from horario_resource import HorarioResource, HorarioListResource


api.add_resource(AdminResource, "/admins")

api.add_resource(UsuarioResource, "/users/<int:id>")
api.add_resource(UsuarioListResource, "/users")

api.add_resource(SalaResource, "/salas/<string:nome>")
api.add_resource(SalaListResource, "/salas")

api.add_resource(HorarioResource, "/horarios/<int:id>")
api.add_resource(HorarioListResource, "/horarios")

if __name__ == '__main__':
	app.run(host=app.config['HOST'],
			port=app.config['PORT'],
			debug=app.config['DEBUG'])
