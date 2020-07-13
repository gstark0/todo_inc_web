from django.shortcuts import render
from django.http import HttpResponse
from .models import List, Task

def show_lists(request):
	lists = List.objects.all()
	return render(template_name='lists.html', request=request, context={'lists': lists})