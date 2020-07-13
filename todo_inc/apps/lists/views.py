from django.shortcuts import render
from django.http import HttpResponse
from .models import List, Task

def show_lists(request):
	lists = List.objects.all()
	return render(template_name='lists.html', request=request, context={'lists': lists})

def render_list(request, code):
	tasks = Task.objects.filter(list_id__code=code)
	list_item = List.objects.get(code=code)
	return render(template_name='list.html', request=request, context={'tasks': tasks, 'list': list_item})