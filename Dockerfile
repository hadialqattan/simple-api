FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app
COPY ./test /test
COPY ./tests /tests 
COPY requirements.txt /

RUN pip install -r /requirements.txt

EXPOSE 80

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8