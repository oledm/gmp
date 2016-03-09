from django.db import models
from django.contrib.postgres.fields import IntegerRangeField, ArrayField

class Organization(models.Model):
    name = models.CharField('Наименование ТГ', max_length=100)
    address = models.CharField('Почтовый адрес', max_length=400)
    phone = models.CharField('Телефон', max_length=100)
    fax = models.CharField('Факс', max_length=20)
    director = models.CharField('Генеральный директор', max_length=50)

    def __str__(self):
        return self.name


class LPU(models.Model):
    name = models.CharField('Наименование ЛПУ MГ', max_length=100)
    organization = models.ForeignKey(
        'Organization',
        verbose_name='Наименование ТГ'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'LPU'
