# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404

from exam.models import Test
from exam.forms import ContactForm
from django.core.mail import send_mail

# Main view that shows all tests created
def index(request):
	# Order available tests by name
	sort_test_list = Test.objects.order_by('name')[:5]

	# Display index.html
	return render(request, 'exam/index.html', {'sort_test_list': sort_test_list})

# View that shows all questions related to a specific test
def questions_test(request, test_id):
    
	# Get the test selected in index.html
	test = get_object_or_404(Test, pk=test_id)

	# Display question_test.html
	return render(request, 'exam/questions_test.html', {'test': test})

# View that shows the results of a specific test
def results(request, test_id):

	# Get the test selected in question_test.html
	test = get_object_or_404(Test, pk=test_id)

	for question in test.question_set.all():
			identificador = question.id
			if request.method=='POST':
				choice=request.POST[identificador]
				response_select = get_object_or_404(Response, pk=choice)
			
	# Display results.html
	return render(request, 'exam/results.html', {'test': test, 'response_select' : response_select})

def contact(request,test_id):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			send_mail(
				cd['subject'],
				cd['message'],
				cd.get('email', 'noreply@example.com'),
				['siteowner@example.com'],
			)
		return HttpResponseRedirect('exam/contact_form.html')
	else:
		form = ContactForm()
	return render(request, 'exam/contact_form.html', {'form': form})
