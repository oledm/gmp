from django.db import models

#from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError

#from django.contrib.postgres.fields import IntegerRangeField

#from psycopg2.extras import NumericRange

class Engine(models.Model):
    name = models.CharField('Тип', max_length=40)
    #temp = IntegerRangeField(
    #    verbose_name='Допустимый диапазон температур окружающей среды',
    #    default='(-40, 40)'
    #)

    scheme = models.ImageField('Конструктивная схема')
    meters = models.ImageField('Толщинометрия')

    ex = models.ForeignKey('ExClass',
        verbose_name='Исполнение по взрывозащите'
    )

    temp_low = models.SmallIntegerField('Нижняя граница допустимого ' + 
        'диапазона температур окружающей среды')
    temp_high = models.SmallIntegerField('Верхняя граница допустимого ' + 
        'диапазона температур окружающей среды')

    factory = models.ForeignKey(
        'Factory',
        verbose_name='Завод изготовитель'
    )

    connection = models.ManyToManyField(
        'Connection', 
        verbose_name='Соединение'
    )

    kpd = models.SmallIntegerField('Коэффициент полезного действия, %')

    coef_power = models.FloatField('Коэффициент мощности, cosφ')

    warming_class = models.ForeignKey(
        'WarmingClass',
        verbose_name='Класс нагревостойкости изоляции'
    )
    
    weight = models.SmallIntegerField('Масса двигателя, кг')
    resistance_wire = models.SmallIntegerField('Сопротивление обмотки, Ом')
    resistance_isolation = models.SmallIntegerField('Сопротивление изоляции, Мом')

    def __str__(self):
        return self.name

    def clean(self):
        if self.kpd > 100 or self.kpd < 0:
            raise ValidationError('Коэффициент полезного действия не может быть более 100%')

        if self.coef_power > 1 or self.coef_power < 0:
            raise ValidationError('Коэффициент мощности должен быть в диапазоне [0...1]')

class Connection(models.Model):
    CONNECTION_TYPES = (
        (1, 'Звезда'),
        (2, 'Треугольник')
    )
    connection_type = models.SmallIntegerField(
            'Название соединения',
            unique=True,
            choices=CONNECTION_TYPES)
    scheme = models.ImageField('Схема соединения')
    
    def __str__(self):
        return self.get_connection_type_display()


class Factory(models.Model):
    name = models.CharField('Наименование завода', unique=True, max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Factories'

class ExClass(models.Model):
    name = models.CharField('Наименование исполнения по взрывозащите',
            unique=True,
            max_length=30
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Ex classes'

class WarmingClass(models.Model):
    warming_class_codes = ('Y', 'A', 'E', 'B', 'F', 'H', 'C')
    CLASSES = tuple(zip(range(0, len(warming_class_codes)), warming_class_codes))

    name = models.SmallIntegerField(
        'Обозначение класса нагревостойкости',
        unique=True,
        choices=CLASSES
    )

    def __str__(self):
        return 'Класс {}'.format(self.get_name_display())

    class Meta:
        verbose_name_plural = 'Warming classes'
