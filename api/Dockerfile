<<<<<<< HEAD
FROM python:3.10.6-alpine3.16
=======
FROM python:3.10.6
>>>>>>> 9c7844b0f8ed0ac8f3b2c8d2c2d7ded091554ab1

COPY requirements.txt /temp/requirements.txt
COPY project-wallet /project-wallet

WORKDIR /project-wallet

EXPOSE 8000
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
<<<<<<< HEAD
RUN pip install --upgrade pip
RUN pip install -r /temp/requirements.txt
=======
RUN wget http://nz2.archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2.19_amd64.deb
RUN apt-get install dpkg -y
RUN apt-get update
RUN apt-get install build-essential -y
RUN dpkg -i libssl1.1_1.1.1f-1ubuntu2.19_amd64.deb
RUN pip install --upgrade pip
RUN pip install -r /temp/requirements.txt
>>>>>>> 9c7844b0f8ed0ac8f3b2c8d2c2d7ded091554ab1
