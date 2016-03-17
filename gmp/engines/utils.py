from random import randrange
from functools import partial
import locale

locale.setlocale(locale.LC_ALL, "")
loc = partial(locale.format, "%.2f")

def moments():
    return {
        # Отношение номинального значения начального пускового момента
        # к номинальному вращающему моменту
        'fraction_nominal_moment': loc(randrange(7, 23)/10),
        # Отношение начального пускового тока к номинальному току
        'fraction_initial_current': loc(randrange(36, 75)/10),
        # Отношение максимального вращающего момента
        # к номинальному вращающему моменту
        'fraction_max_spin_moment': loc(randrange(18, 25)/10),
    }

# Подвижное взрывонепроницаемые соединения
def moveable_Ex_connections():
    def values():
        data = [
            randrange(1538, 1543)/100, # L1
            randrange(2027, 2035)/100, # D
            randrange(2020, 2026)/100, # d
        ]
        data.append(data[1] - data[2]) # W1
        data.append(6.3)               # S
        return tuple(map(lambda x: loc(x), data))

    return {
        # Узел взрывозащиты верхнего подшипникового узла
        'top_point': dict(zip(['L1', 'D', 'd', 'W1', 'S'], values())),
        # Узел взрывозащиты нижнего подшипникового узла
        'bottom_point': dict(zip(['L1', 'D', 'd', 'W1', 'S'], values())),
    }

# Неподвижное взрывонепроницаемое соединения
def unmoveable_Ex_connections():
    def values_out():
        data = [
            randrange(2550, 2558)/100, # L1
            randrange(1247, 1254)/100, # L2
            randrange(3, 6)/100,       # W1
            randrange(63, 68)/10,      # b
            randrange(43, 48)/10,      # a
            1.5,                       # f
            6.3                        # S
        ]
        return tuple(map(lambda x: loc(x), data))

    def values_cap():
        data = [
            randrange(2530, 2548)/100, # L1
            randrange(1287, 1294)/100, # L2
            randrange(3, 6)/100,       # W1
            randrange(83, 88)/10,      # b
            randrange(53, 58)/10,      # a
            1.5,                       # f
            6.3                        # S
        ]
        return tuple(map(lambda x: loc(x), data))

    return {
        # Выводное устройство - крышка
        'out_krishka': dict(zip(['L1', 'L2', 'W1', 'b', 'a', 'f', 'S'], values_out())),
        # Выводное устройство - станина
        'out_stanina': dict(zip(['L1', 'L2', 'W1', 'b', 'a', 'f', 'S'], values_out())),
        # Крышка узла взрывозащиты - подшипниковый щит со стороны привода
        'cap_shield': dict(zip(['L1', 'L2', 'W1', 'b', 'a', 'f', 'S'], values_cap())),
        # Крышка узла взрывозащиты - подшипниковый щит с противо-положной приводу стороны
        'cap_shield_reverse':dict(zip(['L1', 'L2', 'W1', 'b', 'a', 'f', 'S'], values_cap())) 
    }
