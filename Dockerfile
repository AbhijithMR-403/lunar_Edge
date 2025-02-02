FROM python:3.11

WORKDIR /app

COPY requirement.txt .


RUN pip install --no-cache-dir -r requirement.txt

# RUN ["python", "manage.py", "makemigrations"]

# RUN ["python", "manage.py", "migrate"]

COPY . .


EXPOSE 8000:8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
