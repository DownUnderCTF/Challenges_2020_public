FROM ubuntu:18.04 AS build

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update && apt-get install -y \
    autoconf \
    bison \
    flex \
    gcc \
    g++ \
    git \
    libprotobuf-dev \
    libnl-route-3-dev \
    libtool \
    make \
    pkg-config \
    protobuf-compiler
RUN git clone https://github.com/google/nsjail.git /nsjail && cd /nsjail && make

# dpkg --add-architecture i386 && apt-get install -y libc6:i386 for 32 bit
FROM ubuntu:18.04
RUN apt-get update && \
    apt-get install -y libprotobuf10 libnl-route-3-200 && \
    rm -rf /var/lib/apt/lists/*
COPY --from=build /nsjail/nsjail /usr/bin/nsjail
RUN useradd -r -u 1000 ctf
COPY nsjail-pwn.sh /home/ctf/
RUN chmod +x /home/ctf/nsjail-pwn.sh

# run default script
ENTRYPOINT ["/home/ctf/nsjail-pwn.sh"]
