FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    openssh-server \
    python3 \
    python3-pip \
&& rm -rf /var/lib/apt/lists/*

RUN pip3 install asciimatics

COPY ./challenge/ /home/ductf/
RUN chmod +x /home/ductf/shell.py
RUN useradd -ms /home/ductf/shell.py ductf
RUN echo "ductf:ductf" | chpasswd

RUN mkdir /var/run/sshd
RUN sed -i 's/#PasswordAuthentication/PasswordAuthentication/g' /etc/ssh/sshd_config
RUN sed -i 's/#Port 22/Port 1337/g' /etc/ssh/sshd_config
RUN chmod -x /etc/update-motd.d/*

EXPOSE 1337
CMD ["/usr/sbin/sshd", "-D", "-e"]
