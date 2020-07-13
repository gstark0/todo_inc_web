from django.db import models


class List(models.Model):
	name = models.CharField(max_length=50)
	code = models.CharField(max_length=4)

class Task(models.Model):
	name = models.CharField(max_length=50)
	completed = models.BooleanField(default=False)
	list_id = models.ForeignKey(List, on_delete=models.CASCADE)