FROM debian
RUN apt-get update
RUN apt-get install wget -y
RUN apt-get install bzip2 -y
RUN wget https://downloads.getmonero.org/linux64
RUN mkdir monero
RUN tar -xjvf linux64 -C monero
WORKDIR /monero/monero-x86_64-linux-gnu-v0.18.2.2
EXPOSE 18080 18081 28080 28081 38080 38081
