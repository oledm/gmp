from random import randrange

from django.db import models

#from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError

from . import utils

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

    power = models.FloatField('Номинальная мощность, кВт')
    voltage = models.SmallIntegerField('Номинальное напряжение, В')
    current = models.FloatField('Номинальный ток статора, А')
    freq = models.SmallIntegerField('Номинальная частота вращения, об/мин')

    kpd = models.FloatField('Коэффициент полезного действия, %')

    coef_power = models.FloatField('Коэффициент мощности, cosφ')

    warming_class = models.ForeignKey(
        'WarmingClass',
        verbose_name='Класс нагревостойкости изоляции'
    )
    
    weight = models.SmallIntegerField('Масса двигателя, кг')
    #resistance_wire = models.SmallIntegerField('Сопротивление обмотки, Ом')
    resistance_isolation = models.SmallIntegerField('Сопротивление изоляции, Мом')

    def __str__(self):
        return self.name

    @property
    def random_data(self):
        return {
            # Сопротивление обмотки, Ом
            'resistance_wire': '{:.2f}'.format(
                (self.voltage ** 2) /
                (self.power * 1000 * self.coef_power) *
                0.03 * randrange(1000, 1050)/1000
            ),
            'moments': utils.moments(),
            'moveable_Ex_connections': utils.moveable_Ex_connections(),
            'unmoveable_Ex_connections': utils.unmoveable_Ex_connections(),
        }

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
        return '{}'.format(self.get_name_display())

    class Meta:
        verbose_name_plural = 'Warming classes'

class ThermClass(models.Model):
    therm_class_codes = tuple(map(lambda x: 'T' + str(x), range(1,7)))
    CLASSES = tuple(zip(range(0, len(therm_class_codes)), therm_class_codes))

    name = models.SmallIntegerField(
        'Обозначение температурного класса',
        unique=True,
        choices=CLASSES
    )
    t_max = models.PositiveSmallIntegerField('Максимально допустимая температура поверхности оболочки, °C')

    def __str__(self):
        return '{}'.format(self.get_name_display())

    class Meta:
        verbose_name_plural = 'Therm classes'
