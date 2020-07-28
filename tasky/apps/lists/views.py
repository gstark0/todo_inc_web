from django.shortcuts import render
from django.http import HttpResponse
from .models import List, Task
import json

def show_lists(request):
	if 'codes' in request.COOKIES:
		codes = request.COOKIES['codes']
		codes = json.loads(codes)
	else:
		codes = []
	lists = List.objects.filter(code__in=codes)
	return render(template_name='lists.html', request=request, context={'lists': lists})

def render_list(request, code):
	tasks = Task.objects.filter(list_id__code=code)
	list_item = List.objects.get(code=code)
	return render(template_name='list.html', request=request, context={'tasks': tasks, 'list': list_item})