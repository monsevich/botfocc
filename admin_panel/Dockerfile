FROM python:3.11-slim
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV DJANGO_SETTINGS_MODULE=config.settings
RUN python manage.py collectstatic --noinput || true
EXPOSE 8000
CMD ["bash","-lc","python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]
