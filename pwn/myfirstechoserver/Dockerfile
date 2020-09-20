FROM downunderctf/bin-builder AS builder
COPY ./challenge /challenge
WORKDIR /challenge
RUN gcc echos.c -o echos

FROM downunderctf/nsjail
# ensure that libc is consistent, the ubuntu images update sometimes
COPY ./challenge/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=builder /challenge/echos /home/ctf/chal/
COPY challenge/flag.txt /home/ctf/chal/
EXPOSE 1337/tcp
CMD ["/chal/echos"]
