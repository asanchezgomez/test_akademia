from django.db import models

# Create your models here.
class Test(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField()
	
	# Getter name
	def __unicode__(self):
		return (self.name)

class Question(models.Model):
	TEXT = 'text'
	RADIO = 'radio'
	SELECT = 'select'
	SELECT_MULTIPLE = 'select-multiple'
	INTEGER = 'integer'

	QUESTION_TYPES = (
		(TEXT, 'text'),
		(RADIO, 'radio'),
		(SELECT, 'select'),
		(SELECT_MULTIPLE, 'Select Multiple'),
		(INTEGER, 'integer'),
	)

	text = models.TextField()
	required = models.BooleanField()
	test = models.ForeignKey(Test)
	question_type = models.CharField(max_length=200, choices=QUESTION_TYPES, default=TEXT)

	# Getter name
	def __unicode__(self):
		return (self.text)

class Response(models.Model):
	text = models.TextField()
	isCorrect = models.BooleanField()
	question = models.ForeignKey(Question)

	# Getter name
	def __unicode__(self):
		return (self.text)