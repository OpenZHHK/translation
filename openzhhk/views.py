from cStringIO import StringIO
from collections import defaultdict

from flask import Blueprint, request, redirect, render_template, url_for, send_file
from flask.ext.restful import reqparse
from flask.views import MethodView

from openzhhk import true_values
from openzhhk.models import Word
from openzhhk.utils import nocache

views = Blueprint('views', __name__, template_folder='templates')

parser = reqparse.RequestParser()
parser.add_argument('q', required=False, default='')
parser.add_argument('singleword', required=False, default='0')


class ListView(MethodView):
    def get(self):
        args = parser.parse_args()
        sw = 0
        ##if args["q"] == "":
        ##    return redirect("/")
        if args["singleword"] in true_values:
            sw = 1
        if not Word.exists(args["q"]):
            return redirect("/new?q="+args["q"])
        else:
            return render_template('list.html', q=args["q"], sw=sw)


class DetailView(MethodView):
    def get(self, slug):
        word = Word.objects.get_or_404(slug=slug)
        return render_template('detail.html', word=word)


class NewView(MethodView):
    def get(self):
        args = parser.parse_args()
        return render_template('new.html', q=args["q"])


class SearchView(MethodView):
    def get(self):
        return render_template('search.html')


class APIView(MethodView):
    def get(self):
        return render_template('api.html')

class DownloadView(MethodView):
    @nocache
    def get(self):
        words = Word.get_all()
        lines = ""
        for obj in words:
            lines += "i=%s,t=%s,f=%s,ff=%s\n" % (obj.inputtext.encode('utf8'), obj.translation.encode('utf8'), obj.frequency, obj.flags.encode('utf8'))
        sio = StringIO()
        sio.write(lines)
        sio.seek(0)
        return send_file(sio,
                         attachment_filename="database.txt",
                         as_attachment=True)
class StatsView(MethodView):
    def get(self):
        stats = defaultdict()
        if Word.active_objects:
            stats["last_update"] = Word.active_objects.order_by("-updated_at").first().updated_at.strftime("%x %X")
            stats["entries"] = Word.active_objects.count()
            stats["inputs"] = len(Word.active_objects.distinct("inputtext"))
            stats["translations"] = len(Word.active_objects.distinct("translation"))
            stats["ips"] = len(Word.active_objects.distinct("originalip"))
        return render_template('stats.html', stats=stats)


# Register the urls
views.add_url_rule('/', view_func=SearchView.as_view('search'))
views.add_url_rule('/list', view_func=ListView.as_view('list'))
views.add_url_rule('/new', view_func=NewView.as_view('new'))
views.add_url_rule('/stats', view_func=StatsView.as_view('stats'))
views.add_url_rule('/api', view_func=APIView.as_view('api'))
views.add_url_rule('/word/<slug>', view_func=DetailView.as_view('detail'))
views.add_url_rule('/download', view_func=DownloadView.as_view('download'))
