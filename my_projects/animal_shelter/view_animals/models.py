from django.db import models
from django.utils import timezone


class Shelter(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    address = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}, {self.city}'


class Animal(models.Model):
    STATUS_CHOICES = {
        'arrived': 'Прибыло',
        'taken': 'Забрали'
    }

    name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    arrival_date = models.DateField(default=timezone.now)
    weight = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    special_signs = models.CharField(max_length=300, default=None)
    is_arrived = models.CharField(max_length=20, choices=STATUS_CHOICES, default='arrived')
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}, {self.shelter}, {self.is_arrived}'


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name, self.last_name}, {self.shelter}'
