FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY requirements.txt /

RUN pip install -r /requirements.txt
RUN pip install -U pytest

COPY ./app /app
COPY tests_getter.sh /
