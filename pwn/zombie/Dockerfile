FROM downunderctf/bin-builder AS builder
COPY ./challenge /challenge
WORKDIR /challenge/zombie
ARG TOOLCHAIN=stable
RUN echo "Installing rust" && \
apt -y update && \
apt -y install curl && \
curl https://sh.rustup.rs -sSf | sh -s -- --default-toolchain $TOOLCHAIN -y
ENV PATH /root/.cargo/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
RUN cargo build --release

FROM downunderctf/nsjail
COPY --from=builder /challenge/zombie/target/release/zombie /home/ctf/chal/
COPY challenge/flag.txt /home/ctf/chal/

EXPOSE 1337/tcp
CMD ["/chal/zombie"]
