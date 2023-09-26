FROM python:3.11.1-alpine

WORKDIR /app

COPY . /app
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
# RUN pip install -r requirements.txt --no-cache-dir

WORKDIR /app/api_spot

CMD ["gunicorn", "api_spot.wsgi:application", "--bind", "0:8000" ]