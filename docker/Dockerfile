FROM python:3.11

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get upgrade -y

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY online_quantum_tool /online_quantum_tool

WORKDIR /online_quantum_tool

EXPOSE 8000

RUN python manage.py collectstatic --noinput
RUN python manage.py makemigrations

CMD gunicorn --bind 0.0.0.0:8000 --workers=5 quantum.wsgi