# Set the path
import os
import sys

from flask.ext.script import Manager, Server
from faker import Factory
from openzhhk.models import Word
from random import randint

from openzhhk import app, db

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
	use_debugger=True,
	use_reloader=True,
	host=os.getenv('IP', '0.0.0.0'),
	port=int(os.getenv('PORT', 5000))
))


@manager.command
def clean():
	db.connection.drop_database("openzhhk1")


@manager.command
def seed():
	faker = Factory.create()
	for _ in xrange(50):
		word = {'inputtext': faker.word(), 'translation': faker.word(), 'frequency': randint(1, 100),
		        'flags': faker.sentence()}
		word["slug"] = word["inputtext"]
		obj = Word(**word)
		obj.save()

if __name__ == "__main__":
	manager.run()
