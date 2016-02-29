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
        on_delete=models.CASCADE,
        name='Сотрудник'
    )   
    received_at = models.DateField(blank=False, name='Дата выдачи')
    expired_at= models.DateField(blank=False, name='Срок действия')
    control = models.CharField(blank=False, name='Вид контроля', max_length=10)
    degree = models.PositiveSmallIntegerField(blank=False, name='Уровень')
    group = models.PositiveSmallIntegerField(
        blank=False,
        name='Группа ЭБ',
        choices=EB_GROUPS
    )   

