FROM downunderctf/bin-builder AS builder
COPY ./challenge /challenge
WORKDIR /challenge
RUN make

FROM downunderctf/nsjail
COPY --from=builder /challenge/vecc /home/ctf/chal/
COPY challenge/flag.txt /home/ctf/chal/

EXPOSE 1337/tcp
CMD ["/chal/vecc"]
