FROM python:3.11

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get upgrade -y

RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libcairo2 \
    libgobject-2.0-0 \
    libffi-dev

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY online_quantum_tool /online_quantum_tool

WORKDIR /online_quantum_tool

EXPOSE 8000

RUN python manage.py collectstatic --noinput
RUN python manage.py makemigrations

CMD gunicorn --bind 0.0.0.0:8000 --workers=5 quantum.wsgi