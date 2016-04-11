from django.db import models

class Report(models.Model):
    name = models.CharField('Наименование вида очета', max_length=50)
    url = models.CharField('Ссылка на страницу формирования отчета в веб-интерейсе', max_length=100)
    comment = models.CharField('Описание очета', max_length=150, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'
