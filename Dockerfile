FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app
COPY requirements.txt /
COPY tests_getter.sh /

RUN pip install -r /requirements.txt
RUN pip install -U pytest

EXPOSE 80

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
