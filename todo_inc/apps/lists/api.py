import random
import string
import json

from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import List, Task

positive_response = {'response': 1}
negative_response = {'response': 0}

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
			return JsonResponse(positive_response)
		except List.DoesNotExist:
			return JsonResponse(negative_response)

@csrf_exempt
@require_http_methods(['GET', 'POST'])
def general_lists(request):
	# GET all lists from DB
	if request.method == 'GET':
		# Try to get codes from url to confirm if codes exist in DB
		codes = request.GET.get('codes', '')
		if codes is not '':
			codes = codes.split(',')
			lists = List.objects.filter(code__in=codes).values('name', 'code')

			return JsonResponse({'lists': list(lists)})
		# If codes param doesn't exist, just display all lists from DB
		else:
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
	# DELETE a specific task
	if request.method == 'DELETE':
		try:
			task_instance = Task.objects.get(pk=task_id)
			task_instance.delete()
			return JsonResponse(positive_response)
		except Task.DoesNotExist:
			return JsonResponse(negative_response)

@csrf_exempt
@require_http_methods(['GET', 'POST'])
def general_tasks(request):
	# GET all tasks
	if request.method == 'GET':
		all_tasks = Task.objects.all().values('pk', 'name', 'completed', 'list_id__code')
		return JsonResponse({'tasks': list(all_tasks)})
	# Add a new task
	elif request.method == 'POST':
		data = json.loads(request.body)
		task_name = data['name']
		list_code = data['code']
		try:
			list_instance = List.objects.get(code=list_code)
			new_task = Task(name=task_name, list_id=list_instance)
			new_task.save()
			return JsonResponse(positive_response)

		except List.DoesNotExist:
			return JsonResponse(negative_response)

@require_http_methods(['GET'])
def complete_task(request, task_id=None):
	# Mark a task as "completed" (or "not completed" if it was completed before)
	try:
		task_instance = Task.objects.get(pk=task_id)
		task_instance.completed = not task_instance.completed
		task_instance.save()
		return JsonResponse(positive_response)

	except Task.DoesNotExist:
		return JsonResponse(negative_response)
