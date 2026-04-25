"""
Принцип единственной ответственности (SRP).

OtpService отвечает только за генерацию одноразовых числовых
кодов (OTP). Единственная причина для изменения — смена формата
или длины кода.
"""

import random


class OtpService:
    """Отвечает исключительно за генерацию одноразовых паролей."""

    @staticmethod
    def generate(length: int = 6) -> str:
        lower = 10 ** (length - 1)
        upper = 10**length - 1
        return str(random.randint(lower, upper))
