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
form_parser.add_argument('flags', required=False)

parser = reqparse.RequestParser()
parser.add_argument('q', required=False, default='')
parser.add_argument('page', required=False, default=1, type=int)
parser.add_argument('count', required=False, default=5, type=int)
parser.add_argument('singleword', required=False, default="False")
parser.add_argument('sort', required=False, default="inputtext")

get_file_parser = reqparse.RequestParser()
get_file_parser.add_argument('q', required=False, default="")
get_file_parser.add_argument('singleword', required=False, default="False")


def get_word(slug):
    return Word.objects.get_or_404(slug=slug)


def parse_file(file_obj):
    lines = file_obj.read().split("\n")
    mapping = {"i": "inputtext", "f": "frequency", "t": "translation", "ff": "flags", "flags": "flags",
               "inputtext": "inputtext", "frequency": "frequency", "translation": "translation"}
    for line in lines:
        line = line.strip()
        if line:
            word = {}
            for elem in line.split(","):
                key, val = elem.split("=")
                if key in mapping:
                    word_key = mapping[key]
                    word[word_key] = val
            w = (Word(**word))
            w.save()


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
        obj = Word(**args)
        obj.save()
        return jsonify({'status': 'ok', 'word': obj})


class WordFile(Resource):
    @nocache
    def get(self):
        args = get_file_parser.parse_args()
        words = Word.get_all(**args)
        apache = "*****\nCopyright 2016 OpenZHHK.com\n\nLicensed under the Apache License, version 2.0 (the ""License"");\nYou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\nhttp://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an ""AS IS"" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n*****"
        lines = "" + apache
        for obj in words:
            lines += "i=%s,t=%s,f=%s,ff=%s\n" % (obj.inputtext.encode('utf8'), obj.translation.encode('utf8'), obj.frequency, obj.flags.encode('utf8'))
        sio = StringIO()
        sio.write(lines)
        sio.seek(0)
        return send_file(sio,
                         attachment_filename="openzhhk_cantonese_view.txt",
                         as_attachment=True)

    def post(self):
        f = request.files['file']
        objs = parse_file(f)
        return jsonify({'status': 'ok'})


api.add_resource(WordList, '/api/v1/words')
api.add_resource(WordFile, '/api/v1/words_file')
api.add_resource(Words, '/api/v1/word/<slug>')
