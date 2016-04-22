import datetime
from django.db import models

from gmp.reports.models import Report

class Department(models.Model):

    name = models.CharField('Название отдела', max_length=100, unique=True)
    report_types = models.ManyToManyField(Report, verbose_name='Виды отчетов, выпускаемые отделом')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'отдел'
        verbose_name_plural = 'отделы'

class Measurer(models.Model):
    department = models.ForeignKey(
        'Department', 
	verbose_name='Отдел',
        on_delete=models.CASCADE
    )
    name = models.CharField('Наименование прибора', max_length=100)
    model = models.CharField('Тип (марка)', max_length=50, blank=True, null=True)
    serial_number = models.CharField('Заводской номер', max_length=30, blank=True, null=True)
    verification = models.CharField('Свидетельство о поверке', max_length=50, blank=True, null=True)
    expired_at = models.DateField('Дата следующей поверки', max_length=50, blank=True, null=True)

    def __str__(self):
        #return '{} {}, {}'.format(self.name, self.model, self.department.name)
        return '{} {}'.format(self.name, self.model, self.department.name)

    def verbose_info(self):
        first_word, *other_words = self.name.split()
        info = first_word.lower() + ' ' + ' '.join(other_words)
        if self.model:
            info = info + ' ' + self.model
        if self.serial_number:
            info = info + ' зав.&nbsp;№&nbsp;' + self.serial_number
        if self.verification and self.expired_at:
            info = '{}, свидетельство о поверке №&nbsp;{} действительно до&nbsp;{} г.'.format(
                info, self.verification, self.expired_at.strftime('%d.%m.%Y'))
        return info

    def description(self):
        return '{} {}'.format(self.name, self.model)

    def details(self):
        return (
            self.description(),
            self.serial_number,
            self.verification,
            self.expired_at.strftime('%d.%m.%Y'),
        )

    class Meta:
        ordering = ['name', 'serial_number']
        verbose_name = 'прибор'
        verbose_name_plural = 'приборы'
