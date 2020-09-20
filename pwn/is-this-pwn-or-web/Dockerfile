FROM downunderctf/nsjail

RUN apt-get update && apt-get install -y python3 \
    && rm -rf /var/lib/apt/lists/*

COPY challenge/flag.txt /home/ctf/chal/flag.txt
COPY challenge/server.py /home/ctf/chal/server.py
COPY challenge/d8 /home/ctf/chal/d8
COPY challenge/flagprinter /home/ctf/chal/flagprinter
COPY challenge/snapshot_blob.bin /home/ctf/chal/snapshot_blob.bin

EXPOSE 1337/tcp

CMD ["/usr/bin/python3", "/chal/server.py"]
