# Аспект безопасности №2: Контейнеризация (изоляция компонентов).
# Базовый образ — минимальный официальный python:3.12-slim.
FROM python:3.12-slim

# Не пишем .pyc и не буферизуем вывод (удобнее логирование контейнера).
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Сначала зависимости — для эффективного кэширования слоёв.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Затем исходный код приложения.
COPY . .

# Принцип наименьших привилегий: создаём непривилегированного
# пользователя и запускаем процесс от его имени, а не от root.
RUN useradd --create-home --uid 1000 appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
