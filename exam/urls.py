from django.conf.urls import patterns, url

from exam import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
	url(r'^(?P<test_id>\d+)/$', views.questions_test, name='questions_test'),
	url(r'^(?P<test_id>\d+)/results/$', views.results, name='results'),
)
