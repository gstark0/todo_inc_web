from django.shortcuts import render
from django.http import HttpResponse

def show_lists(request):
	return render(template_name='lists.html', request=request)