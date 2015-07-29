# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404

from exam.models import Test

# Main view that shows all tests created
def index(request):
	sort_test_list = Test.objects.order_by('name')[:5]
	context = {'sort_test_list': sort_test_list}
	return render(request, 'exam/index.html', context)

# View that shows all questions related to a specific test
def questions_test(request, test_id):
    try:
        test = Test.objects.get(pk=test_id)
    except Test.DoesNotExist:
        raise Http404
    return render(request, 'exam/questions_test.html', {'test': test})

# View that shows the results of a specific test
def results(request, test_id):
	test = get_object_or_404(Test, pk=test_id)
	#for question in test.question_set.all():
		#selecteds_choices = question.response_set.get(pk=request.POST[question.id])
	id_pregunta = request.POST[1]
	return render(request, 'exam/results.html', {'test': test, 'id_pregunta': id_pregunta })