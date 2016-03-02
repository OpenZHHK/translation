from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)

app.config['MONGODB_DB'] = 'openzhhk1'
app.config['MONGODB_HOST'] = 'localhost'
app.config['MONGODB_PORT'] = 27017
app.config['MONGODB_USERNAME'] = ''
app.config['MONGODB_PASSWORD'] = ''
app.config["SECRET_KEY"] = "KeepThisS3cr3t"

db = MongoEngine(app)

def register_blueprints(app):
    # Prevents circular imports
    from openzhhk.views import views
    app.register_blueprint(views)

register_blueprints(app)

if __name__ == '__main__':
    app.run()