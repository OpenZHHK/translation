from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['MONGODB_DB'] = 'openzhhk1'
app.config['MONGODB_HOST'] = 'localhost'
app.config['MONGODB_PORT'] = 27017
app.config['MONGODB_USERNAME'] = ''
app.config['MONGODB_PASSWORD'] = ''
app.config["SECRET_KEY"] = "KeepThisS3cr3t"
app.config['DEBUG_TB_PANELS'] = ['flask.ext.mongoengine.panels.MongoDebugPanel']

db = MongoEngine(app)
toolbar = DebugToolbarExtension(app)


def register_blueprints(app):
    # Prevents circular imports
    from openzhhk.views import views
    from openzhhk.api import api_bp
    app.register_blueprint(views)
    app.register_blueprint(api_bp)

register_blueprints(app)

if __name__ == '__main__':
    app.run()