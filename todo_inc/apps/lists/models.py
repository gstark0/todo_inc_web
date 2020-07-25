from django.db import models
from django.utils import timezone
import random

def generate_pk():
	number = random.randint(1000, 200000)
	return number

class List(models.Model):
	name = models.CharField(max_length=50)
	code = models.CharField(max_length=4)

class Task(models.Model):
	id = models.CharField(default=generate_pk, primary_key=True, max_length=255, unique=True)
	name = models.CharField(max_length=50)
	completed = models.BooleanField(default=False)
	list_id = models.ForeignKey(List, on_delete=models.CASCADE)