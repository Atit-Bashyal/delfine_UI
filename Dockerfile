# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

EXPOSE 8000

RUN apt-get update -y && apt install -y nano

WORKDIR /app
COPY . .
RUN python3 -m pip install --no-cache-dir --upgrade pip

RUN pip install -r requirements.txt

RUN python3 manage.py migrate

# execute command "python3 manage.py runserver 0.0.0.0:8000" when container starts
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
