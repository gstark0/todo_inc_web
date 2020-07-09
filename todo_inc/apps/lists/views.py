from django.shortcuts import render
from django.http import HttpResponse

def show_lists(request):
	test = '<h1>This is LISTS app</h1>'
	return HttpResponse(test)