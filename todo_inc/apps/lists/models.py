from django.db import models


class list(models.Model):
	name = models.CharField(max_length=50)
	code = models.CharField(max_length=4)

class task(models.Model):
	name = models.CharField(max_length=50)
	completed = models.BooleanField(default=False)