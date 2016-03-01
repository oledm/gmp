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
    employee = models.ForeignKey(
        'authentication.Employee',
        verbose_name='Сотрудник',
        on_delete=models.CASCADE
    )   
    serial_number = models.CharField('№ квалификационного удостоверения',
        max_length=20
    )
    received_at = models.DateField('Дата выдачи', default=date.today)
    expired_at= models.DateField('Срок действия')
    control = models.CharField('Вид контроля', max_length=10)
    degree = models.PositiveSmallIntegerField('Уровень')
    group = models.PositiveSmallIntegerField('Группа ЭБ', choices=EB_GROUPS)   
