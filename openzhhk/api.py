from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify, Blueprint, request
from openzhhk import app
from openzhhk.models import Word

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

parser = reqparse.RequestParser()
parser.add_argument('inputtext', required=True)
parser.add_argument('translation', required=True)
parser.add_argument('frequency', required=False)


def get_word(slug):
    return Word.objects.get_or_404(id=slug)


class Words(Resource):
    def get(self, slug):
        obj = get_word(slug)
        return jsonify({'status': 'ok', 'word': obj})

    def delete(self, slug):
        obj = get_word(slug)
        obj.soft_delete()
        return jsonify({'status': 'ok'})

    def put(self, slug):
        obj = get_word(slug)
        args = parser.parse_args()
        args["lastip"] = request.remote_addr
        obj.update(**args)
        obj.reload()
        return jsonify({'status': 'ok', 'word': obj})


class WordList(Resource):
    def get(self):
        words = Word.objects.all()
        return jsonify({'status': 'ok', 'words': words})

    def post(self):
        args = parser.parse_args()
        args["lastip"] = request.remote_addr
        args["originalip"] = request.remote_addr
        args["slug"] = args["inputtext"]
        obj = Word(**args)
        obj.save()
        return jsonify({'status': 'ok', 'word': obj})

api.add_resource(WordList, '/api/v1/words')
api.add_resource(Words, '/api/v1/words/<slug>')