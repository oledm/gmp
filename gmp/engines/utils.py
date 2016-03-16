from random import randrange

def moments():
    return {
        # Отношение номинального значения начального пускового момента
        # к номинальному вращающему моменту
        'fraction_nominal_moment': randrange(7, 23)/10,
        # Отношение начального пускового тока к номинальному току
        'fraction_initial_current': randrange(36, 75)/10,
        # Отношение максимального вращающего момента
        # к номинальному вращающему моменту
        'fraction_max_spin_moment': randrange(18, 25)/10,
    }

# Подвижное взрывонепроницаемые соединения
def moveable_Ex_connections():
    def values():
        return (
            randrange(1538, 1543)/100,
            randrange(2027, 2035)/100,
            randrange(2020, 2026)/100
        )
    # Узел взрывозащиты верхнего подшипникового узла
    L1, D, d = values()
    top_point = {
        'L1': '{:.2f}'.format(L1),
        'D': '{:.2f}'.format(D),
        'd': '{:.2f}'.format(d),
        'W1': '{:.2f}'.format(D - d),
        'S': '{:.2f}'.format(6.30)
    }

    # Узел взрывозащиты нижнего подшипникового узла
    L1, D, d = values()
    bottom_point = {
        'L1': '{:.2f}'.format(L1),
        'D': '{:.2f}'.format(D),
        'd': '{:.2f}'.format(d),
        'W1': '{:.2f}'.format(D - d),
        'S': '{:.2f}'.format(6.30)
    }

    return {
        'top_point': top_point,
        'bottom_point': bottom_point,
    }

# Неподвижное взрывонепроницаемое соединения
def unmoveable_Ex_connections():
    def values():
        return (
            randrange(2550, 2558)/100,
            randrange(1247, 1254)/100,
            randrange(3, 6)/100,
            randrange(63, 68)/10,
            randrange(43, 48)/10
        )

    # Выводное устройство - крышка
    L1, L2, W1, b, a =  values()
    out_krishka = {
        'L1': '{:.2f}'.format(L1),
        'L2': '{:.2f}'.format(L2),
        'W1': '{:.2f}'.format(W1),
        'b': '{:.2f}'.format(b),
        'a': '{:.2f}'.format(a),
        'f': '{:.2f}'.format(1.5),
        'S': '{:.2f}'.format(6.3)
    }

    # Выводное устройство - станина
    L1, L2, W1, b, a =  values()
    out_stanina = {
        'L1': '{:.2f}'.format(L1),
        'L2': '{:.2f}'.format(L2),
        'W1': '{:.2f}'.format(W1),
        'b': '{:.2f}'.format(b),
        'a': '{:.2f}'.format(a),
        'f': '{:.2f}'.format(1.5),
        'S': '{:.2f}'.format(6.3)
    }

    #################################################################
    def values():
        return (
            randrange(2530, 2548)/100,
            randrange(1287, 1294)/100,
            randrange(3, 6)/100,
            randrange(83, 88)/10,
            randrange(53, 58)/10
        )
    # Крышка узла взрывозащиты - подшипниковый щит со стороны привода
    L1, L2, W1, b, a =  values()
    cap_shield = {
        'L1': '{:.2f}'.format(L1),
        'L2': '{:.2f}'.format(L2),
        'W1': '{:.2f}'.format(W1),
        'b': '{:.2f}'.format(b),
        'a': '{:.2f}'.format(a),
        'f': '{:.2f}'.format(1.5),
        'S': '{:.2f}'.format(6.3)
    }

    # Крышка узла взрывозащиты - подшипниковый щит с противо-положной приводу стороны
    L1, L2, W1, b, a =  values()
    cap_shield_reverse = {
        'L1': '{:.2f}'.format(L1),
        'L2': '{:.2f}'.format(L2),
        'W1': '{:.2f}'.format(W1),
        'b': '{:.2f}'.format(b),
        'a': '{:.2f}'.format(a),
        'f': '{:.2f}'.format(1.5),
        'S': '{:.2f}'.format(6.3)
    }
    return {
        'out_krishka': out_krishka,
        'out_stanina': out_stanina,
        'cap_shield': cap_shield,
        'cap_shield_reverse': cap_shield_reverse
    }
