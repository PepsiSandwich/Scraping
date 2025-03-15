# Используем официальный Python образ
FROM python:3.11

# Устанавливаем рабочую директорию в контейнере как /pyscrap
WORKDIR /pyscrap

# Копируем все файлы из текущей директории (папка с Dockerfile) в контейнер
COPY . /pyscrap

# Переходим в папку Backend
WORKDIR /pyscrap/Backend

# Устанавливаем все зависимости
RUN pip install --no-cache-dir -r /pyscrap/requirements.txt

# Запускаем приложение (предполагая, что файл называется app.py)
CMD ["python", "app.py"]
