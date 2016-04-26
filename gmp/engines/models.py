from random import randrange

from django.db import models
from django.core.exceptions import ValidationError

from .utils import EngineDataGenerator

#from django.core.validators import MaxValueValidator
#from django.contrib.postgres.fields import IntegerRangeField
#from psycopg2.extras import NumericRange

class Engine(EngineDataGenerator, models.Model):
    zones = (
        'подшипниковый щит со стороны привода',
        'крышка коробки выводов',
        'наружная оболочка корпуса статора',
        'подшипниковый щит с противоположной стороны привода'
    )
    ZONES_CHOICES = tuple(zip(range(0, len(zones)), zones))

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
    resistance_isolation = models.SmallIntegerField('Сопротивление изоляции, Мом')

    connection = models.ManyToManyField(
        'Connection', 
        verbose_name='Соединение'
    )

    ###########################################################################

    control_zone_1 = models.SmallIntegerField(
        'Зона контроля 1',
        choices=ZONES_CHOICES,
        default=0
    )
    control_zone_1_low = models.FloatField('Зона контроля 1 / Толщина основного металла, мм (фактическая) / Нижний предел')
    control_zone_1_high = models.FloatField('Зона контроля 1 / Толщина основного металла, мм (фактическая) / Верхний предел')
    control_zone_1_norm = models.FloatField('Зона контроля 1 / Допустимые толщины норма (не менее)')

    control_zone_2 = models.SmallIntegerField(
        'Зона контроля 2',
        choices=ZONES_CHOICES,
        default=1
    )
    control_zone_2_low = models.FloatField('Зона контроля 2 / Толщина основного металла, мм (фактическая) / Нижний предел')
    control_zone_2_high = models.FloatField('Зона контроля 2 / Толщина основного металла, мм (фактическая) / Верхний предел')
    control_zone_2_norm = models.FloatField('Зона контроля 2 / Допустимые толщины норма (не менее)')

    control_zone_3 = models.SmallIntegerField(
        'Зона контроля 3',
        choices=ZONES_CHOICES,
        default=2
    )
    control_zone_3_low = models.FloatField('Зона контроля 3 / Толщина основного металла, мм (фактическая) / Нижний предел')
    control_zone_3_high = models.FloatField('Зона контроля 3 / Толщина основного металла, мм (фактическая) / Верхний предел')
    control_zone_3_norm = models.FloatField('Зона контроля 3 / Допустимые толщины норма (не менее)')

    control_zone_4 = models.SmallIntegerField(
        'Зона контроля 4',
        choices=ZONES_CHOICES,
        default=3
    )
    control_zone_4_low = models.FloatField('Зона контроля 4 / Толщина основного металла, мм (фактическая) / Нижний предел')
    control_zone_4_high = models.FloatField('Зона контроля 4 / Толщина основного металла, мм (фактическая) / Верхний предел')
    control_zone_4_norm = models.FloatField('Зона контроля 4 / Допустимые толщины норма (не менее)')

    ###########################################################################
    moveable_Ex_connections_top_point_L1_low = models.FloatField('Подвижное взрывонепроницаемое соединение / Узел взрывозащиты верхнего подшипникового узла / L1 (нижний предел)', blank=True, null=True)
    moveable_Ex_connections_top_point_L1_high = models.FloatField('Подвижное взрывонепроницаемое соединение / Узел взрывозащиты верхнего подшипникового узла / L1 (верхний предел)', blank=True, null=True)
    moveable_Ex_connections_top_point_D_low = models.FloatField('Подвижное взрывонепроницаемое соединение / Узел взрывозащиты верхнего подшипникового узла / D (нижний предел)', blank=True, null=True)
    moveable_Ex_connections_top_point_D_high = models.FloatField('Подвижное взрывонепроницаемое соединение / Узел взрывозащиты верхнего подшипникового узла / D (верхний предел)', blank=True, null=True)
    moveable_Ex_connections_top_point_d_low = models.FloatField('Подвижное взрывонепроницаемое соединение / Узел взрывозащиты верхнего подшипникового узла / d (нижний предел)', blank=True, null=True)
    moveable_Ex_connections_top_point_d_high = models.FloatField('Подвижное взрывонепроницаемое соединение / Узел взрывозащиты верхнего подшипникового узла / d (верхний предел)', blank=True, null=True)
    moveable_Ex_connections_top_point_S = models.FloatField('Подвижное взрывонепроницаемое соединение / Узел взрывозащиты верхнего подшипникового узла / S', default=6.3, blank=True, null=True)

    ###########################################################################
    moveable_Ex_connections_bottom_point_L1_low = models.FloatField('Подвижное взрывонепроницаемое соединение / Узел взрывозащиты нижнего подшипникового узла / L1 (нижний предел)', blank=True, null=True)
    moveable_Ex_connections_bottom_point_L1_high = models.FloatField('Подвижное взрывонепроницаемое соединение / Узел взрывозащиты нижнего подшипникового узла / L1 (верхний предел)', blank=True, null=True)
    moveable_Ex_connections_bottom_point_D_low = models.FloatField('Подвижное взрывонепроницаемое соединение / Узел взрывозащиты нижнего подшипникового узла / D (нижний предел)', blank=True, null=True)
    moveable_Ex_connections_bottom_point_D_high = models.FloatField('Подвижное взрывонепроницаемое соединение / Узел взрывозащиты нижнего подшипникового узла / D (верхний предел)', blank=True, null=True)
    moveable_Ex_connections_bottom_point_d_low = models.FloatField('Подвижное взрывонепроницаемое соединение / Узел взрывозащиты нижнего подшипникового узла / d (нижний предел)', blank=True, null=True)
    moveable_Ex_connections_bottom_point_d_high = models.FloatField('Подвижное взрывонепроницаемое соединение / Узел взрывозащиты нижнего подшипникового узла / d (верхний предел)', blank=True, null=True)
    moveable_Ex_connections_bottom_point_S = models.FloatField('Подвижное взрывонепроницаемое соединение / Узел взрывозащиты нижнего подшипникового узла / S', default=6.3, blank=True, null=True)

    ###########################################################################
    unmoveable_Ex_connections_out_krishka_L1_low = models.FloatField('Неподвижное взрывонепроницаемое соединение / Выводное устройство - крышка / L1 (нижний предел)', blank=True, null=True)
    unmoveable_Ex_connections_out_krishka_L1_high = models.FloatField('Неподвижное взрывонепроницаемое соединение / Выводное устройство - крышка / L1 (верхний предел)', blank=True, null=True)
    unmoveable_Ex_connections_out_krishka_L2_low = models.FloatField('Неподвижное взрывонепроницаемое соединение / Выводное устройство - крышка / L2 (нижний предел)', blank=True, null=True)
    unmoveable_Ex_connections_out_krishka_L2_high = models.FloatField('Неподвижное взрывонепроницаемое соединение / Выводное устройство - крышка / L2 (верхний предел)', blank=True, null=True)
    unmoveable_Ex_connections_out_krishka_W1_low = models.FloatField('Неподвижное взрывонепроницаемое соединение / Выводное устройство - крышка / W1 (нижний предел)', blank=True, null=True)
    unmoveable_Ex_connections_out_krishka_W1_high = models.FloatField('Неподвижное взрывонепроницаемое соединение / Выводное устройство - крышка / W1 (верхний предел)', blank=True, null=True)
    unmoveable_Ex_connections_out_krishka_b_low = models.FloatField('Неподвижное взрывонепроницаемое соединение / Выводное устройство - крышка / b (нижний предел)', blank=True, null=True)
    unmoveable_Ex_connections_out_krishka_b_high = models.FloatField('Неподвижное взрывонепроницаемое соединение / Выводное устройство - крышка / b (верхний предел)', blank=True, null=True)
    unmoveable_Ex_connections_out_krishka_a_low = models.FloatField('Неподвижное взрывонепроницаемое соединение / Выводное устройство - крышка / a (нижний предел)', blank=True, null=True)
    unmoveable_Ex_connections_out_krishka_a_high = models.FloatField('Неподвижное взрывонепроницаемое соединение / Выводное устройство - крышка / a (верхний предел)', blank=True, null=True)
    unmoveable_Ex_connections_out_krishka_f = models.FloatField('Неподвижное взрывонепроницаемое соединение / Выводное устройство - крышка / f', default=1.5, blank=True, null=True)
    unmoveable_Ex_connections_out_krishka_S = models.FloatField('Неподвижное взрывонепроницаемое соединение / Выводное устройство - крышка / S', default=6.3, blank=True, null=True)

    ###########################################################################
    unmoveable_Ex_connections_out_stanina_L1_low = models.FloatField('Неподвижное взрывонепроницаемое соединение / Выводное устройство - станина / L1 (нижний предел)', blank=True, null=True)
    unmoveable_Ex_connections_out_stanina_L1_high = models.FloatField('Неподвижное взрывонепроницаемое соединение / Выводное устройство - станина / L1 (верхний предел)', blank=True, null=True)
    unmoveable_Ex_connections_out_stanina_L2_low = models.FloatField('Неподвижное взрывонепроницаемое соединение / Выводное устройство - станина / L2 (нижний предел)', blank=True, null=True)
    unmoveable_Ex_connections_out_stanina_L2_high = models.FloatField('Неподвижное взрывонепроницаемое соединение / Выводное устройство - станина / L2 (верхний предел)', blank=True, null=True)
    unmoveable_Ex_connections_out_stanina_W1_low = models.FloatField('Неподвижное взрывонепроницаемое соединение / Выводное устройство - станина / W1 (нижний предел)', blank=True, null=True)
    unmoveable_Ex_connections_out_stanina_W1_high = models.FloatField('Неподвижное взрывонепроницаемое соединение / Выводное устройство - станина / W1 (верхний предел)', blank=True, null=True)
    unmoveable_Ex_connections_out_stanina_b_low = models.FloatField('Неподвижное взрывонепроницаемое соединение / Выводное устройство - станина / b (нижний предел)', blank=True, null=True)
    unmoveable_Ex_connections_out_stanina_b_high = models.FloatField('Неподвижное взрывонепроницаемое соединение / Выводное устройство - станина / b (верхний предел)', blank=True, null=True)
    unmoveable_Ex_connections_out_stanina_a_low = models.FloatField('Неподвижное взрывонепроницаемое соединение / Выводное устройство - станина / a (нижний предел)', blank=True, null=True)
    unmoveable_Ex_connections_out_stanina_a_high = models.FloatField('Неподвижное взрывонепроницаемое соединение / Выводное устройство - станина / a (верхний предел)', blank=True, null=True)
    unmoveable_Ex_connections_out_stanina_f = models.FloatField('Неподвижное взрывонепроницаемое соединение / Выводное устройство - станина / f', default=1.5, blank=True, null=True)
    unmoveable_Ex_connections_out_stanina_S = models.FloatField('Неподвижное взрывонепроницаемое соединение / Выводное устройство - станина / S', default=6.3, blank=True, null=True)

    ###########################################################################
    unmoveable_Ex_connections_cap_shield_L1_low = models.FloatField('Неподвижное взрывонепроницаемое соединение / Крышка узла взрывозащиты - подшипниковый щит со стороны привода / L1 (нижний предел)', blank=True, null=True)
    unmoveable_Ex_connections_cap_shield_L1_high = models.FloatField('Неподвижное взрывонепроницаемое соединение / Крышка узла взрывозащиты - подшипниковый щит со стороны привода / L1 (верхний предел)', blank=True, null=True)
    unmoveable_Ex_connections_cap_shield_L2_low = models.FloatField('Неподвижное взрывонепроницаемое соединение / Крышка узла взрывозащиты - подшипниковый щит со стороны привода / L2 (нижний предел)', blank=True, null=True)
    unmoveable_Ex_connections_cap_shield_L2_high = models.FloatField('Неподвижное взрывонепроницаемое соединение / Крышка узла взрывозащиты - подшипниковый щит со стороны привода / L2 (верхний предел)', blank=True, null=True)
    unmoveable_Ex_connections_cap_shield_W1_low = models.FloatField('Неподвижное взрывонепроницаемое соединение / Крышка узла взрывозащиты - подшипниковый щит со стороны привода / W1 (нижний предел)', blank=True, null=True)
    unmoveable_Ex_connections_cap_shield_W1_high = models.FloatField('Неподвижное взрывонепроницаемое соединение / Крышка узла взрывозащиты - подшипниковый щит со стороны привода / W1 (верхний предел)', blank=True, null=True)
    unmoveable_Ex_connections_cap_shield_b_low = models.FloatField('Неподвижное взрывонепроницаемое соединение / Крышка узла взрывозащиты - подшипниковый щит со стороны привода / b (нижний предел)', blank=True, null=True)
    unmoveable_Ex_connections_cap_shield_b_high = models.FloatField('Неподвижное взрывонепроницаемое соединение / Крышка узла взрывозащиты - подшипниковый щит со стороны привода / b (верхний предел)', blank=True, null=True)
    unmoveable_Ex_connections_cap_shield_a_low = models.FloatField('Неподвижное взрывонепроницаемое соединение / Крышка узла взрывозащиты - подшипниковый щит со стороны привода / a (нижний предел)', blank=True, null=True)
    unmoveable_Ex_connections_cap_shield_a_high = models.FloatField('Неподвижное взрывонепроницаемое соединение / Крышка узла взрывозащиты - подшипниковый щит со стороны привода / a (верхний предел)', blank=True, null=True)
    unmoveable_Ex_connections_cap_shield_f = models.FloatField('Неподвижное взрывонепроницаемое соединение / Крышка узла взрывозащиты - подшипниковый щит со стороны привода / f', default=1.5, blank=True, null=True)
    unmoveable_Ex_connections_cap_shield_S = models.FloatField('Неподвижное взрывонепроницаемое соединение / Крышка узла взрывозащиты - подшипниковый щит со стороны привода / S', default=6.3, blank=True, null=True)

    ###########################################################################
    unmoveable_Ex_connections_cap_shield_reverse_L1_low = models.FloatField('Неподвижное взрывонепроницаемое соединение / Крышка узла взрывозащиты - подшипниковый щит с противоположной приводу стороны / L1 (нижний предел)', blank=True, null=True)
    unmoveable_Ex_connections_cap_shield_reverse_L1_high = models.FloatField('Неподвижное взрывонепроницаемое соединение / Крышка узла взрывозащиты - подшипниковый щит с противоположной приводу стороны / L1 (верхний предел)', blank=True, null=True)
    unmoveable_Ex_connections_cap_shield_reverse_L2_low = models.FloatField('Неподвижное взрывонепроницаемое соединение / Крышка узла взрывозащиты - подшипниковый щит с противоположной приводу стороны / L2 (нижний предел)', blank=True, null=True)
    unmoveable_Ex_connections_cap_shield_reverse_L2_high = models.FloatField('Неподвижное взрывонепроницаемое соединение / Крышка узла взрывозащиты - подшипниковый щит с противоположной приводу стороны / L2 (верхний предел)', blank=True, null=True)
    unmoveable_Ex_connections_cap_shield_reverse_W1_low = models.FloatField('Неподвижное взрывонепроницаемое соединение / Крышка узла взрывозащиты - подшипниковый щит с противоположной приводу стороны / W1 (нижний предел)', blank=True, null=True)
    unmoveable_Ex_connections_cap_shield_reverse_W1_high = models.FloatField('Неподвижное взрывонепроницаемое соединение / Крышка узла взрывозащиты - подшипниковый щит с противоположной приводу стороны / W1 (верхний предел)', blank=True, null=True)
    unmoveable_Ex_connections_cap_shield_reverse_b_low = models.FloatField('Неподвижное взрывонепроницаемое соединение / Крышка узла взрывозащиты - подшипниковый щит с противоположной приводу стороны / b (нижний предел)', blank=True, null=True)
    unmoveable_Ex_connections_cap_shield_reverse_b_high = models.FloatField('Неподвижное взрывонепроницаемое соединение / Крышка узла взрывозащиты - подшипниковый щит с противоположной приводу стороны / b (верхний предел)', blank=True, null=True)
    unmoveable_Ex_connections_cap_shield_reverse_a_low = models.FloatField('Неподвижное взрывонепроницаемое соединение / Крышка узла взрывозащиты - подшипниковый щит с противоположной приводу стороны / a (нижний предел)', blank=True, null=True)
    unmoveable_Ex_connections_cap_shield_reverse_a_high = models.FloatField('Неподвижное взрывонепроницаемое соединение / Крышка узла взрывозащиты - подшипниковый щит с противоположной приводу стороны / a (верхний предел)', blank=True, null=True)
    unmoveable_Ex_connections_cap_shield_reverse_f = models.FloatField('Неподвижное взрывонепроницаемое соединение / Крышка узла взрывозащиты - подшипниковый щит с противоположной приводу стороны / f', default=1.5, blank=True, null=True)
    unmoveable_Ex_connections_cap_shield_reverse_S = models.FloatField('Неподвижное взрывонепроницаемое соединение / Крышка узла взрывозащиты - подшипниковый щит с противоположной приводу стороны / S', default=6.3, blank=True, null=True)



    def __str__(self):
        return self.name

    @property
    def random_data(self):
        return {
            #'elements_condition': self.elements_condition(),
            'moments': self.moments(),
            'moveable_Ex_connections': self.moveable_Ex_connections(),
            'resistance_wire': self.resistance_wire(),
            'unmoveable_Ex_connections': self.unmoveable_Ex_connections(),
        }

    class Meta:
        verbose_name = 'Двигатель'
        verbose_name_plural = 'Двигатели'

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

    class Meta:
        verbose_name = 'Соединение'
        verbose_name_plural = 'Соединения'


class Factory(models.Model):
    name = models.CharField('Наименование завода', unique=True, max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Завод'
        verbose_name_plural = 'Заводы'


class ExClass(models.Model):
    name = models.CharField('Наименование исполнения по взрывозащите',
            unique=True,
            max_length=30
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Класс взрывозащиты'
        verbose_name_plural = 'Классы взрывозащиты'


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
        verbose_name = 'Класс нагревостойкости'
        verbose_name_plural = 'Классы нагревостойкости'

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
        verbose_name = 'Температурный класс'
        verbose_name_plural = 'Температурные классы'
