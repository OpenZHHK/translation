from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify, Blueprint, request, send_file
from openzhhk.models import Word
from cStringIO import StringIO
from utils import nocache

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

form_parser = reqparse.RequestParser()
form_parser.add_argument('inputtext', required=True)
form_parser.add_argument('translation', required=True)
form_parser.add_argument('frequency', required=False)

parser = reqparse.RequestParser()
parser.add_argument('q', required=False, default='')
parser.add_argument('page', required=False, default=1, type=int)
parser.add_argument('count', required=False, default=5, type=int)
parser.add_argument('singleword', required=False, default="False", type=str)

get_file_parser = reqparse.RequestParser()
get_file_parser.add_argument('q', required=False, default="")
get_file_parser.add_argument('singleword', required=False, default="False", type=str)


def get_word(slug):
	return Word.objects.get_or_404(id=slug)


def parse_file(file_obj):
	lines = file_obj.read().split("\n")
	mapping = {"i": "inputtext", "f": "frequency", "t": "translation", "ff": "flags", "flags": "flags",
	           "inputtext": "inputtext", "frequency": "frequency", "translation": "translation"}
	words = []
	for line in lines:
		if line:
			word = {}

			for elem in line.split(","):
				key, val = elem.split("=")
				if key in mapping:
					word_key = mapping[key]
					word[word_key] = val

			print word
			words.append(Word(**word))

	return words


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
		args = form_parser.parse_args()
		args["lastip"] = request.remote_addr
		obj.update(**args)
		obj.reload()
		return jsonify({'status': 'ok', 'word': obj})


class WordList(Resource):
	def get(self):
		args = parser.parse_args()
		words = Word.get_paginated(**args)
		return jsonify({'status': 'ok', 'words': words.items, 'count': words.per_page, 'page': words.page,
		                'pages': words.pages, 'has_next': words.has_next})

	def post(self):
		args = form_parser.parse_args()
		args["lastip"] = request.remote_addr
		args["originalip"] = request.remote_addr
		args["slug"] = args["inputtext"]
		obj = Word(**args)
		obj.save()
		return jsonify({'status': 'ok', 'word': obj})


class WordFile(Resource):
	@nocache
	def get(self):
		args = get_file_parser.parse_args()
		words = Word.get_all(**args)
		lines = ""
		for obj in words:
			lines += "i=%s,t=%s,f=%s,ff=%s\n" % (obj.inputtext, obj.translation, obj.frequency, obj.flags)
		print lines
		sio = StringIO()
		sio.write(lines)
		sio.seek(0)
		return send_file(sio,
		                 attachment_filename="words.txt",
		                 as_attachment=True)

	def post(self):
		f = request.files['file']
		objs = parse_file(f)
		x = Word.objects.insert(objs)
		print x
		return jsonify({'status': 'ok'})


api.add_resource(WordList, '/api/v1/words')
api.add_resource(WordFile, '/api/v1/words_file')
api.add_resource(Words, '/api/v1/word/<slug>')
