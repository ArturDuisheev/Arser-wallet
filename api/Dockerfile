FROM python:3.10.6

COPY requirements.txt /temp/requirements.txt
COPY project-wallet /project-wallet

WORKDIR /project-wallet

EXPOSE 8000
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN wget http://security.ubuntu.com/ubuntu/pool/main/o/openssl/openssl_1.1.1f-1ubuntu2.16_amd64.deb

RUN apt-get install dpkg -y
RUN apt-get update
RUN apt-get install build-essential -y
RUN dpkg -i libssl1.1_1.1.1f-1ubuntu2.16_amd64.deb
RUN pip install --upgrade pip
RUN pip install -r /temp/requirements.txt
