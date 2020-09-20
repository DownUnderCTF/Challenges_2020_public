FROM downunderctf/nsjail

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
&& rm -rf /var/lib/apt/lists/*

RUN pip3 install pycryptodome

COPY ./challenge/ /home/ctf/chal
EXPOSE 1337/tcp

CMD ["/chal/server.py"]
