# FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
# COPY requirements.txt /tmp
# RUN pip install -r /tmp/requirements.txt
# WORKDIR /app
# COPY ./app .

FROM python:3.8-alpine

WORKDIR /myapp

COPY Pipfile* ./

RUN pip install --no-cache-dir pipenv && \
    pipenv install --system --deploy --clear

COPY app .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]