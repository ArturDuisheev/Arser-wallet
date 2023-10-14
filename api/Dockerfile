FROM python:3.10.6-alpine3.16

COPY requirements.txt /temp/requirements.txt
COPY project-wallet /project-wallet

WORKDIR /project-wallet

EXPOSE 8000
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
RUN pip install -r /temp/requirements.txt
RUN wget http://nz2.archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2.19_amd64.deb
RUN sudo dpkg -i libssl1.1_1.1.1f-1ubuntu2.19_amd64.deb