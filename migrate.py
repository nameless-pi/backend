from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from setup import app, db
from models import *
from user_model import Usuario
from horario_model import Horario
from sala_model import Sala
from acesso_model import Acesso

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()