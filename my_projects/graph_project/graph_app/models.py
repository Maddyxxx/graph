from django.db import models


class Graph(models.Model):
    OPERATION_CHOICES = (
        ('1', 'сложение'),
        ('2', 'умножение'),
        ('3', 'подсчет длины вектора')
    )
    vector = models.CharField(
        max_length=100,
        default='[0, 0, 0]',
        verbose_name='последовательность чисел'
    )
    operation = models.CharField(
        max_length=1,
        choices=OPERATION_CHOICES,
        default='+',
        verbose_name='операция')
