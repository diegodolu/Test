
FROM python:3.12.4-slim-bookworm

WORKDIR /app

COPY requirements.txt /app

COPY . .
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

EXPOSE 8000

CMD ["gunicorn", "back.wsgi", "--bind", "0.0.0.0:8000"]
