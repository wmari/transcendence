FROM python:3.9.21-slim-bookworm

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY .  code
WORKDIR /code

EXPOSE 8000

ENTRYPOINT [ "python3", "transcendence/manage.py" ]
CMD [ "runserver", "0.0.0.0:8000" ]