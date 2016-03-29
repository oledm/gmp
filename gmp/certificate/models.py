from datetime import date
from django.db import models


class Certificate(models.Model):
    month = ('Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
        'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь')
    MONTHS = tuple(enumerate(month, start=1))

    employee = models.ForeignKey(
        'authentication.Employee',
        verbose_name='Сотрудник',
        on_delete=models.CASCADE
    )   
    serial_number = models.CharField('№ квалификационного удостоверения',
        max_length=20
    )
    received_at_year = models.PositiveSmallIntegerField('Дата выдачи (год)')
    received_at_month = models.PositiveSmallIntegerField('Дата выдачи (месяц)', 
        choices=MONTHS
    )
    expired_at_year = models.PositiveSmallIntegerField('Срок действия (год)')
    expired_at_month = models.PositiveSmallIntegerField('Срок действия (месяц)',
        choices=MONTHS
    )
    control_types = models.ManyToManyField('ControlType', verbose_name='Вид контроля')
    degree = models.PositiveSmallIntegerField('Уровень')

    def __str__(self):
        return 'Удостоверение № {} ({})'.format(self.serial_number, self.employee.fio())

    def details(self):
        return (
            self.serial_number,
            '{:0>2}.{}'.format(self.received_at_month, self.received_at_year),
            '{:0>2}.{}'.format(self.expired_at_month, self.expired_at_year),
            self.control_types.all(),
            self.degree,
            #self.get_group_display()
        )

class ControlType(models.Model):
    name = models.CharField('Краткое обозначение вида контроля', max_length=20)
    full_name = models.CharField('Полное наименование вида контроля', max_length=50)

    def __str__(self):
        return self.name

class EBcertificate(models.Model):
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
    serial_number = models.CharField('№ удостоверения по ЭБ',
        max_length=20
    )
    received_at = models.DateField('Дата выдачи')
    expired_at = models.DateField('Срок действия')
    group = models.PositiveSmallIntegerField('Группа ЭБ', choices=EB_GROUPS)   

    def __str__(self):
        return 'Удостоверение по ЭБ № {} ({})'.format(self.serial_number, self.employee.fio())
