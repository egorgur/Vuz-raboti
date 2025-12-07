import numpy as np


def objective_function(x, y):
    """
    Вычисляет значение функции I(x) — Функция 1.
    Аргумент: x — скаляр или массив.
    Возвращает: значение функции в точке x.
    """
    exp_coeff = -2.77257

    # Вычисляем экспоненциальный член
    exp_term = np.exp(exp_coeff * x**2)

    # Первое слагаемое: 0.05*(x - 1)^2
    term1 = 0.05 * (x - 1) ** 2

    # Второй множитель: (3 - 2.9 * exp(...))
    factor1 = 3 - 2.9 * exp_term

    # Третий множитель: (1 - cos(x * (4 - 50 * exp(...))))
    inner_cos = x * (4 - 50 * exp_term)
    factor2 = 1 - np.cos(inner_cos)

    return term1 + factor1 * factor2


def rastrigin_2d(x, y):
    """
    Ф3
    Функция Растригина (2D).
    Минимум: I(0, 0) = 0.
    Область: x, y ∈ [-16, 16]
    """
    return 0.1 * x**2 + 0.1 * y**2 - 4 * np.cos(0.8 * x) - 4 * np.cos(0.8 * y) + 8


def rosenbrock(x, y):
    """
    Ф5
    Функция Розенброка (Rosenbrock).
    Минимум: I(1, 1) = 0.
    Область: x, y ∈ [-2, 2]
    """
    return 100 * (y - x**2) ** 2 + (1 - x) ** 2


def sombrero(x, y):
    r = np.sqrt(x**2 + y**2)
    amplitude_mod = 1 + 0.3 * np.sin(0.7 * r)  # модуляция амплитуды
    return amplitude_mod * np.cos(r) ** 2 / (1 + 0.001 * r**2)


def function_12(x1, x2):
    """
    Функция 12.
    Область: x1, x2 ∈ [0, 4]
    """
    term1 = 0.5 * (x1**2 + x1 * x2 + x2**2)

    cos_term1 = np.cos(1.5 * x1) * np.cos(3.2 * x1 * x2) * np.cos(3.14 * x2)
    cos_term2 = np.cos(2.2 * x1) * np.cos(4.8 * x1 * x2) * np.cos(3.5 * x2)

    term2 = 1 + 0.5 * cos_term1 + 0.5 * cos_term2

    return term1 * term2
