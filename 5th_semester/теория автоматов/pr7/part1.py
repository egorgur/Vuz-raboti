class BasePrimitiveFunctions:
    """
    Три базовые примитивно рекурсивные функции:
    1. Нулевая функция Z (или O)
    2. Функция следования S
    3. Функция проекции I^n_k
    """

    @staticmethod
    def zero(*args):
        """
        Нулевая функция: Z() = 0 или O^n(x_1,...,x_n) = 0
        Возвращает 0 для любых аргументов
        """
        return 0

    @staticmethod
    def succ(n):
        """
        Функция следования: S(n) = n + 1
        """
        return n + 1

    @staticmethod
    def proj(k, *args):
        """
        Функция проекции: I^n_k(x_1, ..., x_n) = x_k
        Возвращает k-й аргумент

        Пример: proj(1, a, b, c) = b
        """
        return args[k]


class PrimitiveRecursion(BasePrimitiveFunctions):
    """Функции, построенные через ПРИМИТИВНУЮ РЕКУРСИЮ"""

    def pred(self, n):
        """
        Предшественник через ПРИМИТИВНУЮ РЕКУРСИЮ:
        pred(0) = 0 = Z()
        pred(S(n)) = n = I^2_0(n, pred(n))
        """
        if n == 0:
            return self.zero()
        else:
            prev_result = self.pred(n - 1)
            return self.proj(0, n - 1, prev_result)

    def add(self, x, y):
        """
        Сложение через ПРИМИТИВНУЮ РЕКУРСИЮ:
        add(x, 0) = x = I^1_0(x)              -- базовый случай
        add(x, S(y)) = S(add(x, y))           -- рекурсивный шаг
        """
        if y == 0:
            return self.proj(0, x)
        else:
            return self.succ(self.add(x, y - 1))

    def mult(self, x, y):
        """
        Умножение через ПРИМИТИВНУЮ РЕКУРСИЮ:
        mult(x, 0) = 0 = Z()                  -- базовый случай
        mult(x, S(y)) = add(mult(x, y), x)    -- рекурсивный шаг
        """
        if y == 0:
            return self.zero()
        else:
            return self.add(self.mult(x, y - 1), x)

    def power(self, x, y):
        """
        Возведение в степень через ПРИМИТИВНУЮ РЕКУРСИЮ:
        power(x, 0) = 1 = S(Z())              -- базовый случай
        power(x, S(y)) = mult(power(x, y), x) -- рекурсивный шаг
        """
        if y == 0:
            return self.succ(self.zero())  # S(Z()) = 1
        else:
            return self.mult(self.power(x, y - 1), x)


class Calculator(PrimitiveRecursion):
    """Функции, построенные через СУПЕРПОЗИЦИЮ (композицию)"""

    def square(self, x):
        """
        g(x) = x² через СУПЕРПОЗИЦИЮ
        """
        return self.mult(self.proj(0, x), self.proj(0, x))

    def power_self(self, x):
        """
        f(x) = x^x через СУПЕРПОЗИЦИЮ
        """
        return self.power(self.proj(0, x), self.proj(0, x))

    def cube(self, x):
        """
        c(x) = x³ через СУПЕРПОЗИЦИЮ
        """
        return self.mult(self.square(x), self.proj(0, x))


if __name__ == "__main__":
    calc = Calculator()
    print("Вычислитель x^y")
    examples = [(4, 3), (2, 10), (3, 4)]
    for x, y in examples:
        result = calc.power(x, y)
        print(f"  {x:>4} ^ {y:<4} = {result:>10}")

    print("Вычислитель x^x")
    for x in (1, 2, 3, 4):
        result = calc.power_self(x)
        print(f"  {x:>4} ^ {x:<4} = {result:>10}")
