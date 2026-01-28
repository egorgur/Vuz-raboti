from typing import Any, Literal


class BasePrimitiveFunctions:
    @staticmethod
    def zero(*args) -> Literal[0]:
        """
        Нулевая функция.

        Формальное определение:
            Z(x1,...,xn) = 0

        Пример шага:
            Z(5) = 0
        """
        return 0

    @staticmethod
    def succ(n) -> Any:
        """
        Функция следования.

        Формальное определение:
            S(n) = n + 1

        Пример шага:
            S(2) = 3
        """
        return n + 1

    @staticmethod
    def proj(k, *args) -> Any:
        """
        Функция проекции: возвращает заданный аргумент.

        Формальное определение:
            I^n_k(x1,...,xn) = x_k    (0 <= k < n)

        Пример шага:
            I^3_1(5,7,9) = 7
        """
        if k < 0 or k >= len(args):
            raise IndexError("proj: index out of range")
        return args[k]


class PrimitiveRecursion(BasePrimitiveFunctions):
    def pred(self, n) -> Any | Literal[0]:
        """
        Предшественник через примитивную рекурсию.

        Формальное определение:
            pred(0) = 0
            pred(S(n)) = n

        Пример шага:
            pred(3) = 2
        """
        if n == 0:
            return self.zero()
        else:
            prev_result = self.pred(n - 1)
            return self.proj(0, n - 1, prev_result)

    def add(self, x, y) -> Any:  # # -> Any:
        """
        Сложение через примитивную рекурсию.

        Формальное определение:
            add(x,0) = x
            add(x,S(y)) = S(add(x,y))

        Пример шага:
            add(2, S(2)) = S(add(2,2)) => add(2,3)=5
        """
        if y == 0:
            return self.proj(0, x)
        else:
            return self.succ(self.add(x, y - 1))

    def mult(self, x, y) -> Any | Literal[0]:
        """
        Умножение через примитивную рекурсию.

        Формальное определение:
            mult(x,0) = 0
            mult(x,S(y)) = add(mult(x,y), x)

        Пример шага:
            mult(2,S(1)) = add(mult(2,1),2) => mult(2,2)=4
        """
        if y == 0:
            return self.zero()
        else:
            return self.add(self.mult(x, y - 1), x)

    def power(self, x, y) -> Any | Literal[0]:
        """
        Возведение в степень через примитивную рекурсию.

        Формальное определение:
            power(x,0) = 1
            power(x,S(y)) = mult(power(x,y), x)

        Пример шага:
            power(2,S(2)) = mult(power(2,2),2) => power(2,3)=8
        """
        if y == 0:
            return self.succ(self.zero())
        else:
            return self.mult(self.power(x, y - 1), x)

    def monus(self, x, y) -> int:
        """
        Усечённое вычитание (monus): результат неотрицателен.

        Формальное определение:
            monus(x,0) = x
            monus(0,y) = 0
            monus(x,S(y)) = pred(monus(x,y))

        Пример шага:
            monus(5,S(1)) = pred(monus(5,1)) => monus(5,2)=3
        """
        if y == 0:
            return x
        if x == 0:
            return self.zero()
        return self.pred(self.monus(x, y - 1))

    def abs_diff(self, x, y) -> int:
        """
        Абсолютная разность.

        Формальное определение:
            abs_diff(x,y) = add(monus(x,y), monus(y,x))

        Пример шага:
            abs_diff(2,5) = monus(2,5)+monus(5,2) = 0+3 = 3
        """
        return self.add(self.monus(x, y), self.monus(y, x))

    def div(self, x, y) -> int:
        """
        Целочисленное деление вниз (частное).

        Формальное определение (по соглашению):
            div(x,0) = 0
            div(x,y) = 0, если x < y
            div(x,y) = S(div(monus(x,y), y)), иначе

        Пример шага:
            div(7,S(2)) = S(div(monus(7,3),3)) => div(7,3)=2
        """
        if y == 0:
            return self.zero()
        if x < y:
            return self.zero()
        return self.succ(self.div(self.monus(x, y), y))

    def mod(self, x, y) -> int:
        """
        Остаток от целочисленного деления.

        Формальное определение (по соглашению):
            mod(x,0) = x
            mod(x,y) = x, если x < y
            mod(x,y) = mod(monus(x,y), y), иначе

        Пример шага:
            mod(7,3) = mod(monus(7,3),3) => mod(4,3) => mod(1,3) = 1
        """
        if y == 0:
            return x
        if x < y:
            return x
        return self.mod(self.monus(x, y), y)

    def max(self, x, y) -> int:
        """
        Максимум двух чисел.

        Формальное определение:
            max(x,y) = add(x, monus(y,x))

        Пример шага:
            max(2,5) = 2 + monus(5,2) = 2 + 3 = 5
        """
        return self.add(x, self.monus(y, x))

    def min(self, x, y) -> int:
        """
        Минимум двух чисел.

        Формальное определение:
            min(x,y) = x - monus(x,y)   (реализовано через monus)

        Пример шага:
            min(2,5) = monus(2, monus(2,5)) = monus(2,0) = 2
        """
        return self.monus(x, self.monus(x, y))

    def is_zero(self, n) -> int:
        """
        Характеристическая функция нуля.

        Формальное определение:
            is_zero(0) = 1
            is_zero(S(n)) = 0

        Пример шага:
            is_zero(0) = 1, is_zero(3) = 0
        """
        return 1 if n == 0 else 0

    def sign(self, n) -> int:
        """
        Признак числа (характеристическая функция ненулевого).

        Формальное определение:
            sign(0) = 0
            sign(S(n)) = 1

        Пример шага:
            sign(0)=0, sign(5)=1
        """
        return 0 if n == 0 else 1

    def not_(self, n) -> int:
        """
        Логическое НЕ.

        Формальное определение:
            not_(n) = is_zero(n)

        Пример шага:
            not_(0) = 1, not_(3) = 0
        """
        return self.is_zero(n)

    def and_(self, x, y) -> int:
        """
        Логическое И.

        Формальное определение (через sign):
            and_(x,y) = sign( mult(sign(x), sign(y)) )

        Пример шага:
            and_(2,3) = 1, and_(0,3) = 0
        """
        return self.sign(self.mult(self.sign(x), self.sign(y)))

    def or_(self, x, y) -> int:
        """
        Логическое ИЛИ.

        Формальное определение (через sign):
            or_(x,y) = sign( add(sign(x), sign(y)) )

        Пример шага:
            or_(0,0)=0, or_(0,2)=1
        """
        return self.sign(self.add(self.sign(x), self.sign(y)))

    def xor(self, x, y) -> int:
        """
        Исключающее ИЛИ (по признаку нуля/ненуля).

        Формальное определение:
            xor(x,y) = (sign(x) AND not(sign(y))) + (not(sign(x)) AND sign(y))

        Пример шага:
            xor(0,2)=1, xor(3,5)=0
        """
        sx = self.sign(x)
        sy = self.sign(y)
        return self.add(self.mult(sx, self.not_(sy)), self.mult(self.not_(sx), sy))

    def eq(self, x, y) -> int:
        """
        Характеристическая функция равенства: 1 если x == y иначе 0
        Реализация через усечённое вычитание и сложение:
        eq(x,y) = is_zero( monus(x,y) + monus(y,x) )
        """
        return self.is_zero(self.add(self.monus(x, y), self.monus(y, x)))

    def neq(self, x, y) -> int:
        """
        Характеристическая функция неравенства: 1 если x != y иначе 0
        """
        return self.not_(self.eq(x, y))

    def leq(self, x, y) -> int:
        """
        Характеристическая функция <= : 1 если x <= y иначе 0
        Реализовано как is_zero(monus(x,y)).
        """
        return self.is_zero(self.monus(x, y))

    def geq(self, x, y) -> int:
        """
        Характеристическая функция >= : 1 если x >= y иначе 0
        """
        return self.is_zero(self.monus(y, x))

    def less(self, x, y) -> int:
        """
        Характеристическая функция <: 1 если x < y иначе 0
        """
        return 1 if x < y else 0

    def greater(self, x, y) -> int:
        """
        Характеристическая функция >: 1 если x > y иначе 0
        """
        return 1 if x > y else 0

    def is_even(self, n) -> int:
        """
        Проверка чётности: 1 если n чётное иначе 0
        even(0)=1, even(S(n))=not(even(n))
        """
        if n == 0:
            return 1
        return self.not_(self.is_even(n - 1))

    def is_odd(self, n) -> int:
        """
        Проверка нечётности: 1 если n нечётное иначе 0
        """
        return self.not_(self.is_even(n))

    def double(self, n) -> int:
        """
        Удвоение: 2n
        """
        return self.add(n, n)

    def triple(self, n) -> int:
        """
        Утроение: 3n
        """
        return self.add(self.add(n, n), n)

    def factorial(self, n) -> Any | Literal[0]:
        """
        Факториал через примитивную рекурсию:
        fact(0) = 1
        fact(S(n)) = S(n) * fact(n)
        """
        if n == 0:
            return self.succ(self.zero())
        else:
            return self.mult(n, self.factorial(n - 1))

    def fib(self, n) -> int:
        """
        Числа Фибоначчи через примитивную рекурсию на парах:
        F(0)=0, F(1)=1, F(n+1)=F(n)+F(n-1)
        """

        """
        Формальное определение (через пары):
            F(0) = 0
            F(1) = 1
            F(n+1) = F(n) + F(n-1)

        Реализация выполняет итерацию на парах (a,b) = (F(k),F(k+1)).

        Пример шага:
            fib(4) = 3
        """

        def helper(k, a, b):
            if k == 0:
                return a
            return helper(k - 1, b, self.add(a, b))

        return helper(n, 0, 1)


class Calculator(PrimitiveRecursion):
    def square(self, x) -> Any | Literal[0]:
        """
        g(x) = x² через СУПЕРПОЗИЦИЮ
        """
        return self.mult(self.proj(0, x), self.proj(0, x))

    def power_self(self, x) -> Any | Literal[0]:
        """
        f(x) = x^x через СУПЕРПОЗИЦИЮ
        """
        return self.power(self.proj(0, x), self.proj(0, x))

    def cube(self, x) -> Any | Literal[0]:
        """
        c(x) = x³ через СУПЕРПОЗИЦИЮ
        """
        return self.mult(self.square(x), self.proj(0, x))

    def square_sum(self, x, y) -> int:
        """
        (x+y)^2 через суперпозицию
        """
        return self.square(self.add(x, y))

    def max3(self, x, y, z) -> int:
        """
        max(x,y,z) через суперпозицию
        """
        return self.max(self.max(x, y), z)

    def min3(self, x, y, z) -> int:
        """
        min(x,y,z) через суперпозицию
        """
        return self.min(self.min(x, y), z)


if __name__ == "__main__":
    calc = Calculator()
    print("Вычислитель x - y")
    examples = [(1, 3), (4, 2), (5, 3)]
    for x, y in examples:
        result = calc.monus(x, y)
        print(f"  {x:>4} - {y:<4} = {result:>10}")
