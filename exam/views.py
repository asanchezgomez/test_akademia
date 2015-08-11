# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404

from exam.models import Test,Response
from exam.forms import ContactForm
from django.core.mail import send_mail

from django.contrib import messages

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
	
	# Get the number of questions in the test
	num_questions = test.question_set.count()

	# Create a dictionary for store the answers selected
	dic_answers_user = {}

	# List that stores info to send to the template 
	question_list = {}

	# Initialize number of correct answers
	correct_answers = 0

	# Initialize flag error messages
	msg_flag = 0

	# Iterate through all questions in the test selected
	for question in test.question_set.all():
			# If method is POST
			if request.method=='POST':

				# Get the choice through POST
				try:
					choice=request.POST[unicode(question.id)]
					#choice=request.POST[unicode(question.id)]
					response_selected = get_object_or_404(Response, pk=choice)
					#Response.objects.filter(pk=choice).update(isChecked='True')
					#Response.objects.update(isChecked='False')
					response_selected.isChecked = True
					response_selected.save()

					# Get the answer selected for each question
					if response_selected.isCorrect:
						correct_answers = correct_answers + 1
				
					# Store in a list some info that will show in results.html
					question_list = [question.text, response_selected.text, response_selected.isCorrect]

					# Search the correct answer
					for response in question.response_set.all():
						if response.isCorrect:
							question_list.append(response.text)

					# Store the results in the dictionary
					dic_answers_user[question.id] = question_list
				except Exception as e:
					# Agregar campo checked en response, y que en questions_test.html compruebe
					# el campo y lo muestre seleccionado o no. En admin, quitar campo checked. "update django boolean"
					# https://docs.djangoproject.com/en/dev/ref/contrib/messages/#using-messages-in-views-and-templates
					if msg_flag == 0:
						messages.warning(request, 'You have to answer all questions.')
						msg_flag = msg_flag + 1
					
				
	
	# If at least one question is not answered, the user will stay in the same page
	if msg_flag > 0:
		return render(request, 'exam/questions_test.html',{'test': test})

	# Otherwise
	else:		
		# Set all questions unchecked
		for question in test.question_set.all():
			for response in question.response_set.all():
				response.isChecked = False
				response.save()

		# Display results.html
		return render(request, 'exam/results.html', {'test': test, 'dic_answers_user' : dic_answers_user, 'num_questions' : num_questions, 'correct_answers' : correct_answers})
