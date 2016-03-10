from datetime import datetime
from openzhhk import db
from mongoengine_extras.fields import AutoSlugField
from mongoengine import signals, queryset_manager, Q


class Word(db.Document):
	inputtext = db.StringField(required=True)
	translation = db.StringField(required=True)
	frequency = db.IntField(required=True, default=0, min_value=0)
	flags = db.StringField(required=False, default="")
	originalip = db.StringField(required=True, default='0.0.0.0')
	lastip = db.StringField(required=True, default='0.0.0.0')
	deleted = db.BooleanField(default=False)
	singleword = db.BooleanField(default=True)
	created_at = db.DateTimeField(default=datetime.now())
	updated_at = db.DateTimeField(default=datetime.now())
	slug = AutoSlugField()

	@queryset_manager
	def active_objects(self, queryset):
		return queryset.filter(deleted=False)

	# @queryset_manager
	# def get_by_(self, queryset):
	#     return queryset.filter(deleted=False)

	@classmethod
	def get_paginated(cls, page=1, q='', count=5, singleword=False):
		if count > 50:
			count = 50
		if q != "":
			return cls.active_objects(Q(singleword=singleword) & (Q(inputtext__icontains=q) |
			                                                      Q(translation__icontains=q))).paginate(page, count)
		else:
			return cls.active_objects.paginate(page, count)

	@classmethod
	def pre_save(cls, sender, document, **kwargs):
		document.updated_at = datetime.now()
		document.singleword = len(document.inputtext.split()) == 1

	meta = {
		'indexes': ['inputtext', 'deleted', 'singleword', 'frequency', 'slug'],
		'ordering': ['inputtext', '-frequency']
	}

	def soft_delete(self):
		self.update(deleted=True)

	def __unicode__(self):
		return self.inputtext

	def title(self):
		return self.inputtext


signals.pre_save.connect(Word.pre_save, sender=Word)
