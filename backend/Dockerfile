FROM python:3.10-alpine
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["gunicorn", "sport_hub.wsgi:application", "--bind", "0:8000"]
