FROM python:3.11.1-alpine

WORKDIR /app

COPY requirements.txt /app
RUN python -m pip install --upgrade pip
RUN pip install -r /app/requirements.txt --no-cache-dir

COPY ./ /app

WORKDIR /app/api_spot

CMD ["gunicorn", "api_spot.wsgi:application", "--bind", "0:8000" ]