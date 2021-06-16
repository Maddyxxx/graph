from django.db import models


class Graph(models.Model):

    OPERATION_CHOICES = (
        ('add', 'Сложение'),
        ('mul', 'Умножение'),
        ('length', 'Подсчет длины')
    )

    operation = models.CharField(
        max_length=20,
        choices=OPERATION_CHOICES,
        default='add',
        verbose_name='Операция')

    def __str__(self):
        return f'Граф № {self.id}, операция: {self.operation}'


class Vector(models.Model):
    graph = models.ForeignKey(
        Graph,
        on_delete=models.CASCADE,
        default='1',
        verbose_name='Узел')

    vector = models.CharField(
        max_length=100,
        default='1, 2, 3',
        verbose_name='Вектор')

    def __str__(self):
        return f'{self.graph}, {self.vector}'
