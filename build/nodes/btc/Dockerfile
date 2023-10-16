FROM homebrew/ubuntu22.04
RUN sudo apt-get update -y
RUN sudo apt-get install build-essential -y
RUN sudo apt-get install libtool autotools-dev autoconf -y
RUN sudo apt-get install libssl-dev -y
RUN sudo apt-get install libboost-all-dev -y
RUN sudo apt-get install software-properties-common -y
RUN sudo add-apt-repository ppa:luke-jr/bitcoincore -y
RUN sudo apt-get update -y
RUN sudo apt-get install bitcoind -y

RUN mkdir ~/.bitcoin/
COPY bitcoin.conf ~/.bitcoin/
WORKDIR ~/.bitcoin/
