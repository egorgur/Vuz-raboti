# ============================================================================
# ВТОРАЯ ЧАСТЬ
# ============================================================================

from enum import Enum
from typing import Dict, List, Tuple


def some_function(a, b):
    """
    Функция для интерпретации
    """
    c = a + b
    d = a * c
    e = b - a
    f = c * d
    g = a + d
    h = e * f
    i = g - b
    j = h + i
    k = d * e
    result = j + k
    return result

class Sign(Enum):
    """
    Абстрактная область знаков для абстрактной интерпретации.
    """
    UNKNOWN = "UNKNOWN"   # Неопределенное
    NEGATIVE = "-"        # Отрицательное
    ZERO = "0"            # Ноль
    POSITIVE = "+"        # Положительное


class SignAnalysis:
    """
    Абстрактная интерпретация для анализа знаков переменных.
    """
    
    @staticmethod
    def abstract(value: int) -> Sign:
        """Абстракция конкретного значения"""
        if value < 0:
            return Sign.NEGATIVE
        elif value == 0:
            return Sign.ZERO
        else:
            return Sign.POSITIVE
    
    @staticmethod
    def join(s1: Sign, s2: Sign) -> Sign:
        """Операция объединения (join) в решетке знаков."""
        if s1 == s2:
            return s1
        if s1 == Sign.UNKNOWN:
            return s2
        if s2 == Sign.UNKNOWN:
            return s1
        return Sign.UNKNOWN
    
    @staticmethod
    def add(s1: Sign, s2: Sign) -> Sign:
        """Абстрактное сложение"""
        if s1 == Sign.UNKNOWN or s2 == Sign.UNKNOWN:
            return Sign.UNKNOWN
        if s1 == Sign.ZERO:
            return s2
        if s2 == Sign.ZERO:
            return s1
        if s1 == s2:
            return s1
        return Sign.UNKNOWN
    
    @staticmethod
    def sub(s1: Sign, s2: Sign) -> Sign:
        """Абстрактное вычитание"""
        if s1 == Sign.UNKNOWN or s2 == Sign.UNKNOWN:
            return Sign.UNKNOWN
        
        neg_s2 = SignAnalysis.negate(s2)
        return SignAnalysis.add(s1, neg_s2)
    
    @staticmethod
    def mult(s1: Sign, s2: Sign) -> Sign:
        """Абстрактное умножение"""
        if s1 == Sign.UNKNOWN or s2 == Sign.UNKNOWN:
            return Sign.UNKNOWN
        if s1 == Sign.ZERO or s2 == Sign.ZERO:
            return Sign.ZERO
        if s1 == s2:
            return Sign.POSITIVE
        return Sign.NEGATIVE
    
    @staticmethod
    def div(s1: Sign, s2: Sign) -> Sign:
        """Абстрактное деление"""
        if s1 == Sign.UNKNOWN or s2 == Sign.UNKNOWN:
            return Sign.UNKNOWN
        if s2 == Sign.ZERO:
            return Sign.UNKNOWN
        if s1 == Sign.ZERO:
            return Sign.ZERO
        if s1 == s2:
            return Sign.POSITIVE
        return Sign.NEGATIVE
    
    @staticmethod
    def negate(s: Sign) -> Sign:
        """Абстрактное отрицание"""
        if s == Sign.POSITIVE:
            return Sign.NEGATIVE
        if s == Sign.NEGATIVE:
            return Sign.POSITIVE
        return s
    
    @staticmethod
    def power(base: Sign, exp: Sign) -> Sign:
        """Абстрактное возведение в степень"""
        if base == Sign.UNKNOWN or exp == Sign.UNKNOWN:
            return Sign.UNKNOWN
        if exp == Sign.ZERO:
            return Sign.POSITIVE
        if base == Sign.ZERO:
            return Sign.ZERO
        if base == Sign.POSITIVE:
            return Sign.POSITIVE
        if base == Sign.NEGATIVE:
            return Sign.UNKNOWN
        return Sign.UNKNOWN

class AbstractInterpreter:
    """
    Абстрактный интерпретатор для анализа знаков переменных в программе.
    """
    
    def __init__(self):
        self.variables: Dict[str, Sign] = {}
        self.trace: List[Tuple[int, str, str, Sign]] = []
    
    def set_var(self, line: int, name: str, expr: str, sign: Sign):
        """Установить абстрактное значение переменной и записать в трассу"""
        self.variables[name] = sign
        self.trace.append((line, name, expr, sign))
    
    def get_var(self, name: str) -> Sign:
        """Получить абстрактное значение переменной"""
        return self.variables.get(name, Sign.UNKNOWN)
    
    def analyze_some_function(self, a_sign: Sign, b_sign: Sign) -> Dict[str, Sign]:
        """
        Абстрактная интерпретация функции some_function.
        
        Анализируемая программа:
        
        def some_function(a, b):
            c = a + b
            d = a * c
            e = b - a
            f = c * d
            g = a + d
            h = e * f
            i = g - b
            j = h + i
            k = d * e
            result = j + k
            return result
        """
        self.variables = {}
        self.trace = []
        
        self.variables['a'] = a_sign
        self.variables['b'] = b_sign
        
        c = SignAnalysis.add(self.get_var('a'), self.get_var('b'))
        self.set_var(1, 'c', 'a + b', c)
        
        d = SignAnalysis.mult(self.get_var('a'), self.get_var('c'))
        self.set_var(2, 'd', 'a * c', d)
        
        e = SignAnalysis.sub(self.get_var('b'), self.get_var('a'))
        self.set_var(3, 'e', 'b - a', e)
        
        f = SignAnalysis.mult(self.get_var('c'), self.get_var('d'))
        self.set_var(4, 'f', 'c * d', f)
        
        g = SignAnalysis.add(self.get_var('a'), self.get_var('d'))
        self.set_var(5, 'g', 'a + d', g)
        
        h = SignAnalysis.mult(self.get_var('e'), self.get_var('f'))
        self.set_var(6, 'h', 'e * f', h)
        
        i = SignAnalysis.sub(self.get_var('g'), self.get_var('b'))
        self.set_var(7, 'i', 'g - b', i)
        
        j = SignAnalysis.add(self.get_var('h'), self.get_var('i'))
        self.set_var(8, 'j', 'h + i', j)
        
        k = SignAnalysis.mult(self.get_var('d'), self.get_var('e'))
        self.set_var(9, 'k', 'd * e', k)
        
        result = SignAnalysis.add(self.get_var('j'), self.get_var('k'))
        self.set_var(10, 'result', 'j + k', result)
        
        return self.variables.copy()
    
    def print_trace(self):
        """Вывести трассу выполнения"""
        print("\nТрассировка абстрактной интерпретации:")
        print("-" * 60)
        print(f"{'Строка':<8} {'Переменная':<12} {'Выражение':<15} {'Знак':<10}")
        print("-" * 60)
        for line, var, expr, sign in self.trace:
            sign_str = sign.value
            print(f"{line:<8} {var:<12} {expr:<15} {sign_str:<10}")
    
    def print_results(self):
        """Вывести итоговые знаки всех переменных"""
        print("\nИтоговые знаки переменных:")
        print("=" * 50)
        
        sign_names = {
            Sign.POSITIVE: "положительный",
            Sign.NEGATIVE: "отрицательный", 
            Sign.ZERO: "ноль",
            Sign.UNKNOWN: "неизвестен"
        }
        
        for var in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'result']:
            if var in self.variables:
                sign = self.variables[var]
                print(f"  {var:10} = {sign.value:5} ({sign_names[sign]})")


def main():
    print("=" * 70)
    print("ЧАСТЬ 2: АБСТРАКТНАЯ ИНТЕРПРЕТАЦИЯ")
    print("Определение знаков переменных")
    print("=" * 70)
    
    # Вывод анализируемой функции
    print("\nАнализируемая функция (10 строк кода без комментариев):")
    print("-" * 70)
    print("""
def some_function(a, b):
    c = a + b
    d = a * c
    e = b - a
    f = c * d
    g = a + d
    h = e * f
    i = g - b
    j = h + i
    k = d * e
    result = j + k
    return result
""")
    
    # Создаём интерпретатор
    interpreter = AbstractInterpreter()
    
    # Тестовые случаи для абстрактного анализа
    test_cases = [
        (Sign.POSITIVE, Sign.POSITIVE, "a > 0, b > 0"),
        (Sign.POSITIVE, Sign.NEGATIVE, "a > 0, b < 0"),
        (Sign.NEGATIVE, Sign.POSITIVE, "a < 0, b > 0"),
        (Sign.NEGATIVE, Sign.NEGATIVE, "a < 0, b < 0"),
        (Sign.ZERO, Sign.POSITIVE, "a = 0, b > 0"),
        (Sign.POSITIVE, Sign.ZERO, "a > 0, b = 0"),
        (Sign.ZERO, Sign.NEGATIVE, "a = 0, b < 0"),
        (Sign.NEGATIVE, Sign.ZERO, "a < 0, b = 0"),
        (Sign.ZERO, Sign.ZERO, "a = 0, b = 0"),
    ]
    
    for a_sign, b_sign, description in test_cases:
        print("\n" + "=" * 70)
        print(f"ТЕСТ: {description}")
        print(f"Входные значения: a = {a_sign.value}, b = {b_sign.value}")
        print("=" * 70)
        
        # Выполняем абстрактную интерпретацию
        interpreter.analyze_some_function(a_sign, b_sign)
        
        # Выводим результаты
        interpreter.print_trace()
        interpreter.print_results()


if __name__ == "__main__":
    main()
