FROM python:3.7-alpine

WORKDIR /ssti
COPY fl4g.txt /
COPY requirements.txt /ssti
RUN pip install -r requirements.txt

ADD app /ssti

RUN mkdir /db && mv /ssti/templatedb.db /db
RUN addgroup -S ctf \
 && adduser -S ctf -G ctf \
 && chmod 700 /db/templatedb.db \
 && chown ctf.ctf /db/templatedb.db /db


USER ctf
EXPOSE 5000
CMD ["sh", "run.sh"]
