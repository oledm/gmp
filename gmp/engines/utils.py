from random import uniform
from functools import partial
import locale

from django.db import models

locale.setlocale(locale.LC_ALL, "")
loc = partial(locale.format, "%.2f")

def localize(data):
    return tuple(map(lambda x: loc(x) if x else '&ndash;', data))

def rnd(low, high):
    return uniform(low, high) if low and high else None

class EngineDataGenerator(models.Model):

    class Meta:
        abstract = True

    def moments(self):
        return {
            # Отношение номинального значения начального пускового момента
            # к номинальному вращающему моменту
            'fraction_nominal_moment': loc(rnd(0.7, 2.3)),
            # Отношение начального пускового тока к номинальному току
            'fraction_initial_current': loc(rnd(3.6, 7.5)),
            # Отношение максимального вращающего момента
            # к номинальному вращающему моменту
            'fraction_max_spin_moment': loc(rnd(1.8, 2.5)),
        }

    # Сопротивление обмотки, Ом
    def resistance_wire(self):
        return loc(
            (self.voltage ** 2) /
            (self.power * 1000 * self.coef_power) *
            0.03 * rnd(1, 1.05)
        )

    # Подвижное взрывонепроницаемые соединения
    def moveable_Ex_connections(self):
        return {
            # Узел взрывозащиты верхнего подшипникового узла
            'top_point': dict(zip(('L1', 'D', 'd', 'W1', 'S'), self.values_top_point())),
            # Узел взрывозащиты нижнего подшипникового узла
            'bottom_point': dict(zip(('L1', 'D', 'd', 'W1', 'S'), self.values_bottom_point())),
        }

    # Неподвижное взрывонепроницаемое соединения
    def unmoveable_Ex_connections(self):
        return {
            # Выводное устройство - крышка
            'out_krishka': dict(zip(('L1', 'L2', 'W1', 'b', 'a', 'f', 'S'), self.values_out_krishka())),
            # Выводное устройство - станина
            'out_stanina': dict(zip(('L1', 'L2', 'W1', 'b', 'a', 'f', 'S'), self.values_out_stanina())),
            # Крышка узла взрывозащиты - подшипниковый щит со стороны привода
            'cap_shield': dict(zip(('L1', 'L2', 'W1', 'b', 'a', 'f', 'S'), self.values_cap_shield())),
            # Крышка узла взрывозащиты - подшипниковый щит с противо-положной приводу стороны
            'cap_shield_reverse':dict(zip(('L1', 'L2', 'W1', 'b', 'a', 'f', 'S'), self.values_cap_shield_reverse())) 
        }

    # Техническое состояние элементов
    def elements_condition(self):
        return {
            'width_real': dict(zip(('shield', 'cap', 'external', 'shield_reverse'), self.width_real())),
            'width_norm': dict(zip(('shield', 'cap', 'external', 'shield_reverse'), self.width_norm())),
        }

    '''
        Helper functions
    '''
    def width_real(self):
        data = (
            rnd(self.elements_condition_width_real_shield_low,
                self.elements_condition_width_real_shield_high),
            rnd(self.elements_condition_width_real_cap_low,
                self.elements_condition_width_real_cap_high),
            rnd(self.elements_condition_width_real_external_low,
                self.elements_condition_width_real_external_high),
            rnd(self.elements_condition_width_real_shield_reverse_low,
                self.elements_condition_width_real_shield_reverse_high),
        )
        return localize(data)

    def width_norm(self):
        data = (
            self.elements_condition_width_norm_shield,
            self.elements_condition_width_norm_cap,
            self.elements_condition_width_norm_external,
            self.elements_condition_width_norm_shield_reverse,
        )
        return localize(data)


    def values_top_point(self):
        data = [
            rnd(self.moveable_Ex_connections_top_point_L1_low,
                self.moveable_Ex_connections_top_point_L1_high),
            rnd(self.moveable_Ex_connections_top_point_D_low,
                self.moveable_Ex_connections_top_point_D_high),
            rnd(self.moveable_Ex_connections_top_point_d_low,
                self.moveable_Ex_connections_top_point_d_high),
        ]
        data.append(data[1] - data[2])
        data.append(self.moveable_Ex_connections_top_point_S)
        return localize(data)

    def values_bottom_point(self):
        data = [
            rnd(self.moveable_Ex_connections_bottom_point_L1_low,
                self.moveable_Ex_connections_bottom_point_L1_high),
            rnd(self.moveable_Ex_connections_bottom_point_D_low,
                self.moveable_Ex_connections_bottom_point_D_high),
            rnd(self.moveable_Ex_connections_bottom_point_d_low,
                self.moveable_Ex_connections_bottom_point_d_high),
        ]
        data.append(data[1] - data[2])
        data.append(self.moveable_Ex_connections_bottom_point_S)
        return localize(data)


    def values_out_krishka(self):
        data = (
            rnd(self.unmoveable_Ex_connections_out_krishka_L1_low,
                self.unmoveable_Ex_connections_out_krishka_L1_high),
            rnd(self.unmoveable_Ex_connections_out_krishka_L2_low,
                self.unmoveable_Ex_connections_out_krishka_L2_high),
            rnd(self.unmoveable_Ex_connections_out_krishka_W1_low,
                self.unmoveable_Ex_connections_out_krishka_W1_high),
            rnd(self.unmoveable_Ex_connections_out_krishka_b_low,
                self.unmoveable_Ex_connections_out_krishka_b_high),
            rnd(self.unmoveable_Ex_connections_out_krishka_a_low,
                self.unmoveable_Ex_connections_out_krishka_a_high),
            self.unmoveable_Ex_connections_out_krishka_f,
            self.unmoveable_Ex_connections_out_krishka_S,
        )
        return localize(data)

    def values_out_stanina(self):
        data = (
            rnd(self.unmoveable_Ex_connections_out_stanina_L1_low,
                self.unmoveable_Ex_connections_out_stanina_L1_high),
            rnd(self.unmoveable_Ex_connections_out_stanina_L2_low,
                self.unmoveable_Ex_connections_out_stanina_L2_high),
            rnd(self.unmoveable_Ex_connections_out_stanina_W1_low,
                self.unmoveable_Ex_connections_out_stanina_W1_high),
            rnd(self.unmoveable_Ex_connections_out_stanina_b_low,
                self.unmoveable_Ex_connections_out_stanina_b_high),
            rnd(self.unmoveable_Ex_connections_out_stanina_a_low,
                self.unmoveable_Ex_connections_out_stanina_a_high),
            self.unmoveable_Ex_connections_out_stanina_f,
            self.unmoveable_Ex_connections_out_stanina_S,
        )
        return localize(data)

    def values_cap_shield(self):
        data = (
            rnd(self.unmoveable_Ex_connections_cap_shield_L1_low,
                self.unmoveable_Ex_connections_cap_shield_L1_high),
            rnd(self.unmoveable_Ex_connections_cap_shield_L2_low,
                self.unmoveable_Ex_connections_cap_shield_L2_high),
            rnd(self.unmoveable_Ex_connections_cap_shield_W1_low,
                self.unmoveable_Ex_connections_cap_shield_W1_high),
            rnd(self.unmoveable_Ex_connections_cap_shield_b_low,
                self.unmoveable_Ex_connections_cap_shield_b_high),
            rnd(self.unmoveable_Ex_connections_cap_shield_a_low,
                self.unmoveable_Ex_connections_cap_shield_a_high),
            self.unmoveable_Ex_connections_cap_shield_f,
            self.unmoveable_Ex_connections_cap_shield_S,
        )
        return localize(data)

    def values_cap_shield_reverse(self):
        data = (
            rnd(self.unmoveable_Ex_connections_cap_shield_reverse_L1_low,
                self.unmoveable_Ex_connections_cap_shield_reverse_L1_high),
            rnd(self.unmoveable_Ex_connections_cap_shield_reverse_L2_low,
                self.unmoveable_Ex_connections_cap_shield_reverse_L2_high),
            rnd(self.unmoveable_Ex_connections_cap_shield_reverse_W1_low,
                self.unmoveable_Ex_connections_cap_shield_reverse_W1_high),
            rnd(self.unmoveable_Ex_connections_cap_shield_reverse_b_low,
                self.unmoveable_Ex_connections_cap_shield_reverse_b_high),
            rnd(self.unmoveable_Ex_connections_cap_shield_reverse_a_low,
                self.unmoveable_Ex_connections_cap_shield_reverse_a_high),
            self.unmoveable_Ex_connections_cap_shield_reverse_f,
            self.unmoveable_Ex_connections_cap_shield_reverse_S,
        )
        return localize(data)
