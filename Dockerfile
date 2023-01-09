FROM python:3.8.3-slim-buster

WORKDIR /app

COPY notify.py .
COPY requirements.txt .

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "notify.py"]