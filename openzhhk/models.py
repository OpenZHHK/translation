import re
from datetime import datetime
from openzhhk import db, true_values
from mongoengine_extras.fields import SlugField
from mongoengine import signals, queryset_manager, Q

from openzhhk.utils import slugify


class Word(db.Document):
    inputtext = db.StringField(required=True, unique_with="translation")
    translation = db.StringField(required=True, unique_with="inputtext")
    frequency = db.IntField(required=True, default=0, min_value=0)
    flags = db.StringField(required=False, default="")
    originalip = db.StringField(required=True, default='0.0.0.0')
    lastip = db.StringField(required=True, default='0.0.0.0')
    deleted = db.BooleanField(default=False)
    singleword = db.BooleanField(default=True)
    created_at = db.DateTimeField(default=datetime.now())
    updated_at = db.DateTimeField(default=datetime.now())
    slug = SlugField(required=True, unique=True)

    @classmethod
    def _generate_slug(cls, field, value):
        count = 1
        slug = slug_attempt = slugify(value)
        while cls.objects(**{field: slug_attempt}).count() > 0:
            slug_attempt = '%s-%s' % (slug, count)
            count += 1
        return slug_attempt

    @queryset_manager
    def active_objects(self, queryset):
        return queryset.filter(deleted=False)


    @classmethod
    def exists(cls, q=''):
        return cls.active_objects(Q(inputtext__iexact=q) | Q(translation__iexact=q)).count() > 0

    @classmethod
    def get_objects(cls, q='', singleword="False"):
        if q != "":
            if singleword in true_values:
                return cls.active_objects(
                    Q(singleword=True) & (Q(inputtext__iexact=q) | Q(translation__iexact=q)))
            else:
                return cls.active_objects(Q(inputtext__iexact=q) | Q(translation__iexact=q))
        else:
            if singleword in true_values:
                return cls.active_objects(singleword=True)
            else:
                return cls.active_objects

    @classmethod
    def get_all(cls, q='', singleword="False"):
        return cls.get_objects(q, singleword).all()

    @classmethod
    def get_paginated(cls, page=1, q='', count=5, singleword="False", sort="inputtext"):
        if count > 50:
            count = 50
        return cls.get_objects(q, singleword).order_by(sort).paginate(page, count)

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.updated_at = datetime.now()
        document.singleword = len(document.inputtext.split()) == 1
        document.slug = cls._generate_slug("slug", document.inputtext)

    meta = {
        'indexes': ['inputtext', 'translation', 'deleted', 'singleword', 'frequency', 'slug'],
        'ordering': ['inputtext', '-frequency']
    }

    def soft_delete(self):
        self.update(deleted=True)

    def __unicode__(self):
        return self.inputtext or u''

    def title(self):
        return self.inputtext


signals.pre_save.connect(Word.pre_save, sender=Word)
