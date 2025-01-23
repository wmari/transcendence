FROM python:3.9.21-slim-bookworm

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY .  code
WORKDIR /code

EXPOSE 8000

ENTRYPOINT [ "bash", "transcendence/django_script.sh" ]
CMD [ "runserver", "0.0.0.0:8000" ]