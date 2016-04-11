from django.db import models

class Container(models.Model):
    name = models.CharField('Тип оборудования', max_length=50)
    desc = models.CharField('Описание оборудования', max_length=150)
    factory = models.OneToOneField(
        'Factory',
        verbose_name='Завод-изготовитель'
    )
    serial_number = models.CharField('Заводской номер', max_length=50)
    scheme = models.CharField('Номер чертежа', max_length=50)
    reg_number = models.CharField('Регистрационный номер', max_length=50)
    inv_number = models.CharField('Инвентарный номер', max_length=50)
    manufactured_year = models.PositiveSmallIntegerField('Год изготовления')
    started_year = models.PositiveSmallIntegerField('Год ввода в эксплуатацию')
    # Working conditions
    p_work = models.FloatField('Давление рабочее, МПа')
    p_test = models.FloatField('Давление пробное, МПа')
    temp_carrier_low = models.SmallIntegerField('Рабочая температура среды (нижняя граница), ⁰С')
    temp_carrier_high = models.SmallIntegerField('Рабочая температура среды (верхняя граница), ⁰С')
    carrier = models.OneToOneField(
        'Carrier',
        verbose_name='Технологическая среда'
    )
    danger_class = models.PositiveSmallIntegerField('Класс опасности технологической среды по ГОСТ 12.1.007-76')
    volume = models.FloatField('Объем рабочий, м3')
    weight = models.PositiveSmallIntegerField('Масса сосуда (пустого), кг')
    mode = models.CharField('Режим нагружения', max_length=50)
    dimensions_width_ring = models.PositiveSmallIntegerField('Внутренний диаметр обечайки, мм')
    dimensions_width_bottom = models.PositiveSmallIntegerField('Внутренний диаметр днища, мм')
    dimensions_height_ring = models.PositiveSmallIntegerField('Высота обечайки, мм')
    dimensions_height_bottom = models.PositiveSmallIntegerField('Высота днища, мм')
    dimensions_height_total = models.PositiveSmallIntegerField('Высота сосуда (общая)')
    dimensions_side_ring = models.PositiveSmallIntegerField('Толщина стенок обечайки (проектная), мм')
    dimensions_side_bottom = models.PositiveSmallIntegerField('Толщина стенок днища (проектная), мм')
    material_ring = models.OneToOneField(
        'Material',
        verbose_name='Материал обечайки',
        related_name='material_ring'
    )
    material_bottom = models.OneToOneField(
        'Material',
        verbose_name='Материал днища',
        related_name='material_bottom'
    )
    welding = models.OneToOneField(
        'Welding',
        verbose_name='Сведения о сварке'
    )
    control = models.OneToOneField(
        'Control',
        verbose_name='Контроль при изготовлении'
    )

    def __str__(self):
        return '{} ({} зав№ {}, рег.№ {}, инв.№ {})'.format(
            self.desc.capitalize(),
            self.name.lower(),
            self.serial_number,
            self.reg_number,
            self.inv_number,
        )

    class Meta:
        verbose_name = 'Сосуд'
        verbose_name_plural = 'Сосуды'

class Factory(models.Model):
    name = models.CharField('Наименование завода', unique=True, max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Завод-изготовитель'
        verbose_name_plural = 'Заводы-изготовители'

class Carrier(models.Model):
    name = models.CharField('Тип носителя', unique=True, max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Носитель'
        verbose_name_plural = 'Носители'

class Material(models.Model):
    name = models.CharField('Наименование материала', unique=True, max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'

class Welding(models.Model):
    name = models.CharField('Вид сварки', max_length=150)
    material = models.CharField('Материал сварки', max_length=150)

    def __str__(self):
        return '{} ({})'.format(self.name, self.material)

    class Meta:
        verbose_name = 'Сварка'
        verbose_name_plural = 'Сварка'

class Control(models.Model):
    name = models.CharField('Метод контроля при изготовлении', max_length=150)
    area = models.CharField('Объем контроля при изготовлении', max_length=150)

    def __str__(self):
        return '{} {}'.format(self.name, self.area)

    class Meta:
        verbose_name = 'Контроль'
        verbose_name_plural = 'Контроль'
