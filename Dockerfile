# Используем базовый образ Python
FROM python:3.9-slim

# Установка переменной окружения PYTHONUNBUFFERED для вывода логов сразу
ENV PYTHONUNBUFFERED 1

# Установка рабочей директории в /app
WORKDIR /app

# Копирование зависимостей в образ (requirements.txt)
COPY requirements.txt .

# Установка зависимостей проекта
RUN pip install -r requirements.txt

# Копирование всего содержимого текущей директории в /app/
COPY . .

# Экспозиция порта 8000 для работы Django
EXPOSE 8000

CMD ["bash", "-c", "python vtb_ad_generation_lct/manage.py migrate && python vtb_ad_generation_lct/manage.py runserver 0.0.0.0:8000"]

