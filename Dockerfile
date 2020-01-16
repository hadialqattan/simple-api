FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY requirements.txt /

RUN pip install -r /requirements.txt

COPY ./app /app

ENV PYTHONPATH=/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5057"]
