from django.db import models

class Pet(models.Model):
    name = models.CharField(max_length=200)
    breed = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    age = models.DecimalField(max_digits=7, decimal_places=5)
    weight = models.DecimalField(max_digits=8, decimal_places=5)
    location = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    status = models.IntegerField()

class PollRecord(models.Model):
    retrievaltime = models.DateTimeField('retrieval time')