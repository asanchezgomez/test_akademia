from django.contrib import admin
from exam.models import Test, Question, Response
from nested_inlines.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline

class ResponseInline(NestedTabularInline):
	model = Response
	extra = 0

class QuestionInline(NestedTabularInline):
	model = Question
	extra = 0
	inlines = [ResponseInline,]
	
class TestAdmin(NestedModelAdmin):
	inlines = [QuestionInline,]

admin.site.register(Test, TestAdmin)
