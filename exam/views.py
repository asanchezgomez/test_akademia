# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404

from exam.models import Test,Response
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
	
	# Get the number of questions in the test
	num_questions = test.question_set.count()

	# Create a dictionary for store the answers selected
	dic_answers_user = {}

	# List that stores info to send to the template 
	question_list = {}

	# Initialize number of correct answers
	correct_answers = 0

	# Iterate through all questions in the test selected
	for question in test.question_set.all():
			if request.method=='POST':
				# Get the answer selected for each question
				choice=request.POST[question.text]
				response_selected = get_object_or_404(Response, pk=choice)

				# Increment the number of correct answers
				if response_selected.isCorrect:
					correct_answers = correct_answers + 1
				
				#dic_answers_user[question.id] = [response_selected.isCorrect, response_selected.text]
				question_list = [question.text, response_selected.text, response_selected.isCorrect]

				# Search the correct answer
				for response in question.response_set.all():
					if response.isCorrect:
						question_list.append(response.text)

				# Store the results in the dictionary
				dic_answers_user[question.id] = question_list
			
	# Display results.html
	return render(request, 'exam/results.html', {'test': test, 'dic_answers_user' : dic_answers_user, 'num_questions' : num_questions, 'correct_answers' : correct_answers})
