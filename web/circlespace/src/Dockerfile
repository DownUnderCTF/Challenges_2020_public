FROM python:slim-buster

WORKDIR /app
RUN pip install gevent gunicorn

COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app

USER 1000:1000
EXPOSE 5000/tcp

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
