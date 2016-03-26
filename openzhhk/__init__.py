from flask import Flask
from flask.ext.mongoengine import MongoEngine
import os

app = Flask(__name__)

app.config['MONGODB_DB'] = os.getenv('MONGODB_DB', "openzhhk1")
app.config['MONGODB_HOST'] = os.getenv('MONGODB_HOST', "localhost")
app.config['MONGODB_PORT'] = int(os.getenv('MONGODB_PORT', "27017"))
app.config['MONGODB_USERNAME'] = os.getenv('MONGODB_USERNAME', "")
app.config['MONGODB_PASSWORD'] = os.getenv('MONGODB_PASSWORD', "")
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY', "KeepThisS3cr3t")

db = MongoEngine(app)

true_values = ["true", "True", "1", "on", "On"]


def register_blueprints(app):
    # Prevents circular imports
    from openzhhk.views import views
    from openzhhk.api import api_bp
    app.register_blueprint(views)
    app.register_blueprint(api_bp)

register_blueprints(app)

if __name__ == '__main__':
    app.run()