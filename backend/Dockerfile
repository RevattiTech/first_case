FROM python:3.12

WORKDIR /backend

COPY req.txt ./

RUN pip install -r req.txt

COPY . .


CMD gunicorn -w 1 -b 0.0.0.0:8000  main:app
