# Generated by Django 3.2.3 on 2021-06-05 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graph_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graph',
            name='operation',
            field=models.CharField(choices=[('1', 'сложение'), ('2', 'умножение'), ('3', 'подсчет длины вектора')], default='+', max_length=1, verbose_name='операция'),
        ),
    ]
