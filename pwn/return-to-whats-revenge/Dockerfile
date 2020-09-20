FROM downunderctf/nsjail
COPY ./challenge/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY ./challenge/return-to-whats-revenge /home/ctf/chal/
COPY challenge/flag.txt /home/ctf/chal/
EXPOSE 1337/tcp
CMD ["/chal/return-to-whats-revenge"]
