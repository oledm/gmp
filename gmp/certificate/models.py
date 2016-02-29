from datetime import date
from django.db import models


class Certificate(models.Model):
    EB_GROUPS = ( 
        (1, 'I'),
        (2, 'II'),
        (3, 'III'),
        (4, 'IV'),
        (5, 'V'),
    )
    employee = models.ForeignKey('authentication.Employee',
        blank=False,
        verbose_name='Сотрудник',
        on_delete=models.CASCADE
    )   
    received_at = models.DateField('Дата выдачи', blank=False, default=date.today)
    expired_at= models.DateField('Срок действия', blank=False)
    control = models.CharField('Вид контроля', blank=False, max_length=10)
    degree = models.PositiveSmallIntegerField('Уровень', blank=False)
    group = models.PositiveSmallIntegerField('Группа ЭБ',
        blank=False,
        choices=EB_GROUPS
    )   

