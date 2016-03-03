from django.db import models
from django.contrib.postgres.fields import IntegerRangeField, ArrayField

class Engine(models.Model):
    CONNECTION_TYPES = (
        ('s', 'Звезда'),
        ('t', 'Треугольник')
    )
    name = models.CharField('Тип', max_length=40)
    exp = models.CharField('Исполнение по взрывозащите', max_length=30)
    temp = IntegerRangeField('Допустимый диапазон температур окружающей среды')

    #temp_low = models.SmallIntegerField('Нижняя граница допустимого ' + 
    #    'диапазона температур окружающей среды', max_length=30)
    #temp_high = models.SmallIntegerField('Верхняя граница допустимого ' + 
    #    'диапазона температур окружающей среды', max_length=30)
    factory = models.CharField('Завод изготовитель', max_length=50)
    connection = ArrayField(
        models.CharField(
            'Соединение фаз',
            choices=CONNECTION_TYPES,
            max_length=50
        )
    )