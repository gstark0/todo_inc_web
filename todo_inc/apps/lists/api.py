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

def specific_task(request, task_id=None):
	pass


def general_tasks(request):
	pass
