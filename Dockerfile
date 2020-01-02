FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7


COPY ./app /app
COPY ./db /db 
COPY ./test /test
COPY ./tests /tests 
COPY requirements.txt /

RUN pip install -r /requirements.txt
