# Create your views here.
from django.http import HttpResponse

from exam.models import Test

def index(request):
	sort_test_list = Test.objects.order_by('-name')[:5]
	output = ', '.join([p.name for p in sort_test_list])
	return HttpResponse(output)
