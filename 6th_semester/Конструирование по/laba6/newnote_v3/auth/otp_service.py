"""Сервис генерации одноразовых кодов."""

import random


class OtpService:
    """Генерация OTP-кодов."""

    @staticmethod
    def generate(length: int = 6) -> str:
        lower = 10 ** (length - 1)
        upper = 10**length - 1
        return str(random.randint(lower, upper))
