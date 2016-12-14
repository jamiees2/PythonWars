from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from pythonwars.models import db
from pythonwars.routes import pythonwars

manager = Manager(pythonwars)
migrate = Migrate(pythonwars, db)
manager.add_command('db', MigrateCommand)
if __name__ == '__main__':
    manager.run()
