from datetime import datetime
from openzhhk import db
from mongoengine_extras.fields import AutoSlugField
# from flask import url_for


class Word(db.Document):
    inputtext = db.StringField(required=True)
    translation = db.StringField(required=True)
    frequency = db.IntField(required=True, default=0, min_value=0)
    flags = db.StringField(required=False)
    originalip = db.StringField(required=True, default='0.0.0.0')
    lastip = db.StringField(required=True, default='0.0.0.0')
    deleted = db.BooleanField(default=False)
    singleword = db.BooleanField(default=True)
    created_at = db.DateTimeField(default=datetime.now())
    updated_at = db.DateTimeField(default=datetime.now())
    slug = AutoSlugField(populate_from='inputtext')

    def pre_save(cls, sender, document, **kwargs):
        document.updated_at = datetime.now()
        document.singleword = len(document.inputtext.split()) == 1

    meta = {
        'indexes': ['inputtext', 'deleted', 'singleword', 'frequency','slug'],
        'ordering': ['-frequency']
    }

    def __unicode__(self):
        return self.inputtext
