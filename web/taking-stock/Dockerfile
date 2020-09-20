FROM python:3.8-slim-buster as base
FROM base as build

RUN pip install --prefix=/build --no-warn-script-location gunicorn[gevent]
COPY meta/requirements.txt /tmp/requirements.txt
RUN pip install --prefix=/build --no-warn-script-location -r /tmp/requirements.txt

FROM base as dist

COPY --from=build /build /usr/local

COPY meta/entrypoint.sh /
COPY meta/flag /flag_aR4EfMH98EsNz1mg0bSITg
COPY src/ /app/

RUN groupadd ctf \
 && useradd -g ctf ctf \
 && chown -R ctf.ctf /app

USER ctf
WORKDIR /app
EXPOSE 8000
ENTRYPOINT ["sh", "/entrypoint.sh"]