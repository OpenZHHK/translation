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

env = os.getenv('ENV', "development")
dev = env == "development"
prod = env == "production"

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
	use_debugger=dev,
	use_reloader=dev,
	host=os.getenv('IP', '0.0.0.0'),
	port=int(os.getenv('PORT', 5000))
))


@manager.command
def clean():
	db.connection.drop_database("openzhhk1")


@manager.command
def soft_clean():
	words = Word.active_objects.all()
	for word in words:
		word.soft_delete()


@manager.command
def seed():
	faker = Factory.create()
	for _ in xrange(50):
		word = {'inputtext': faker.word(), 'translation': faker.word(), 'frequency': randint(1, 100),
		        'flags': faker.sentence()}
		obj = Word(**word)
		obj.save()
	for _ in xrange(50):
		word = {'inputtext': ' '.join(faker.words(2)), 'translation': ' '.join(faker.words()), 'frequency': randint(1, 100),
		        'flags': faker.sentence()}
		obj = Word(**word)
		obj.save()

if __name__ == "__main__":
	manager.run()
