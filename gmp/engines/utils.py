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

# Подвижные взрывонепроницаемые соединения
def moveable_Ex_connections():
    L1 = randrange(1538, 1543)/100

    # Узел взрывозащиты верхнего подшипникового узла
    D = randrange(2027, 2035)/100
    d = randrange(2020, 2026)/100
    top_point = {
        'L1': L1,
        'D': D,
        'd': d,
        'W1': '{:.2f}'.format(D - d),
        'S': 6.3
    }

    # Узел взрывозащиты нижнего подшипникового узла
    D = randrange(2025, 2028)/100
    d = randrange(2020, 2024)/100
    bottom_point = {
        'L1': L1,
        'D': D,
        'd': d,
        'W1': '{:.2f}'.format(D - d),
        'S': 6.3
    }

    return {
        'top_point': top_point,
        'bottom_point': bottom_point,
    }
