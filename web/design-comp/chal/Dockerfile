FROM python:3.8-slim-buster AS base

RUN pip install --prefix=/build --no-warn-script-location gunicorn[gevent]

COPY meta/requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt && rm -r /tmp/requirements.txt

COPY meta/flag /flag
COPY src/ /app/
WORKDIR /app/

ENTRYPOINT ["gunicorn", "-k", "gevent", "-b", "0.0.0.0:8000", "--access-logfile", "-", "app:app"]