FROM python:3.9-alpine

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY ./tests /code/tests

CMD uvicorn app.main:app --reload --proxy-headers --host 0.0.0.0 --port $PORT