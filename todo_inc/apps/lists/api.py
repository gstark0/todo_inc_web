import random
import string
import json

from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import List, Task

@csrf_exempt
@require_http_methods(['GET', 'DELETE'])
def specific_list(request, code=None):
	# GET tasks from a specific list
	if request.method == 'GET':
		data = Task.objects.filter(list_id__code=code).values('pk', 'name', 'completed')
		return JsonResponse({'tasks': list(data)})
	# DELETE a specific list
	elif request.method == 'DELETE':
		try:
			list_instance = List.objects.get(code=code)
			list_instance.delete()
			return JsonResponse({'response': 1})
		except List.DoesNotExist:
			return JsonResponse({'response': 0})

@csrf_exempt
@require_http_methods(['GET', 'POST'])
def general_lists(request):
	# GET all lists from DB
	if request.method == 'GET':
		all_lists = List.objects.all().values('code', 'name')
		return JsonResponse({'lists': list(all_lists)})

	# Generate a new list and return its code
	elif request.method == 'POST':
		letters = string.ascii_letters
		random_code = ''.join(random.choice(letters) for i in range(4))
		name = json.loads(request.body)['name']

		new_list = List(name=name, code=random_code)
		new_list.save()

		return JsonResponse({'code': random_code, 'response': 1})


@csrf_exempt
@require_http_methods(['DELETE'])
def specific_task(request, task_id=None):
	if request.method == 'DELETE':
		try:
			task_instance = Task.objects.get(pk=task_id)
			task_instance.delete()
			return JsonResponse({'response': 1})
		except Task.DoesNotExist:
			return JsonResponse({'response': 0})

@csrf_exempt
@require_http_methods(['GET', 'POST'])
def general_tasks(request):
	if request.method == 'GET':
		all_tasks = Task.objects.all().values('pk', 'name', 'completed', 'list_id__code')
		return JsonResponse({'tasks': list(all_tasks)})
	elif request.method == 'POST':
		data = json.loads(request.body)
		task_name = data['name']
		list_code = data['code']
		try:
			list_instance = List.objects.get(code=list_code)
			new_task = Task(name=task_name, list_id=list_instance)
			new_task.save()
			return JsonResponse({'response': 1})

		except List.DoesNotExist:
			return JsonResponse({'response': 0})

@require_http_methods(['GET'])
def complete_task(request, task_id=None):
	try:
		task_instance = Task.objects.get(pk=task_id)
		task_instance.completed = not task_instance.completed
		task_instance.save()
		return JsonResponse({'response': 1})

	except Task.DoesNotExist:
		return JsonResponse({'response': 0})
