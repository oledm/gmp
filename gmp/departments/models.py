from django.db import models

class Instrument(models.Model):
    department = models.ForeignKey(
        'authentication.Department', 
	verbose_name='Отдел',
        on_delete=models.CASCADE
    )
    name = models.CharField('Наименование прибора', max_length=100)
    model = models.CharField('Тип (марка)', max_length=50)
    serial_number = models.CharField('Заводской номер', max_length=30)
    verification = models.CharField('Свидетельство о поверке', max_length=50)
    expired_at = models.DateField('Дата следующей поверки', max_length=50)

    def __str__(self):
        return '{} ({}), {}'.format(self.name, self.model, self.department.name)
