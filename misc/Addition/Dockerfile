FROM tiangolo/uwsgi-nginx-flask:python3.8

ENV LISTEN_PORT 1337
ENV UWSGI_INI /uwsgi.ini

RUN apt update \
 && apt install -y \
      python3-flask \
      python3-pip \
 && rm -rf /var/lib/apt/lists/*
RUN pip3 install flask_wtf

RUN groupadd --gid 1000 ctf \
 && useradd --no-create-home -g ctf -u 1000 ctf

COPY ./meta/uwsgi.ini /uwsgi.ini
RUN rm /app/uwsgi.ini

COPY ./challenge/app /app


EXPOSE 1337