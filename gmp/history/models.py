from django.db import models
from django.contrib.postgres.fields import JSONField

class Input(models.Model):
    obj_model = JSONField()
    date = models.DateTimeField('Время сохранения объекта', auto_now=True)
    employee = models.ForeignKey(
        'authentication.employee',
        verbose_name='Сотрудник',
        on_delete=models.CASCADE
    )
