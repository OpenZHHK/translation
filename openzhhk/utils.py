from flask import make_response
from functools import wraps, update_wrapper
from datetime import datetime
import re
import unicodedata

STRIP_REGEXP = re.compile(r'[^\w\s-]')
HYPHENATE_REGEXP = re.compile(r'[-\s]+')


def slugify(value):
    if not isinstance(value, unicode):
        value = unicode(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(STRIP_REGEXP.sub('', value).strip().lower())
    return HYPHENATE_REGEXP.sub('-', value)


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)