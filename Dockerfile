# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

ENV PYTHONIOENCODING=utf-8

COPY requirements.txt .
RUN pip3 install -r requirements.txt

ADD . .

CMD ["python3", "-m" , "main.py", "run"]