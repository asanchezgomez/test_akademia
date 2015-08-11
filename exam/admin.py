from django.contrib import admin
from exam.models import Test, Question, Response
from nested_inlines.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline
from django.forms import TextInput, Textarea
from django.db import models

class ResponseInline(NestedTabularInline):
	model = Response
	extra = 0
	formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':40})},
    }
	fieldsets = [
        (None,               {'fields': ['text']}),
		(None,               {'fields': ['isCorrect']}),
    ]

class QuestionInline(NestedTabularInline):
	model = Question
	extra = 0
	inlines = [ResponseInline,]
	formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':40})},
    }
	
class TestAdmin(NestedModelAdmin):
	inlines = [QuestionInline,]
	fieldsets = [
        (None,               {'fields': ['name']}),
    ]
	formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':40})},
    }

admin.site.register(Test, TestAdmin)
