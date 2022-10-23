FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE=yes

WORKDIR /app

COPY .pdbrc.py /root
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY weather/ ./weather
