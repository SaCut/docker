# syntax=docker/dockerfile:1
FROM python:3
# FROM ubuntu:20.04

# label is a good practice, though optional
LABEL MAINTAINER = scutrupi@spartaglobal.com

# RUN apt-get update -y && apt-get upgrade -y
RUN apt-get update \
    && apt-get install unixodbc -y \
    && apt-get install unixodbc-dev -y \
    && apt-get install freetds-dev -y \
    && apt-get install freetds-bin -y \
    && apt-get install tdsodbc -y \
    && apt-get install --reinstall build-essential -y

# populate "ocbcinst.ini" as this is where ODBC driver config sits
RUN echo "[FreeTDS]\n\
Description=FreeTDS Driver\n\
Driver=/usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so\n\
Setup=/usr/lib/x86_64-linux-gnu/odbc/libtdsS.so" >> /etc/odbcinst.ini

# RUN apt-get install -y python3 python3-pip python3-dev

# copy the requirements file
COPY ./requirements.txt .

# intalling requirements
RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of the repo
COPY ./plane_task /

# set working directory
# WORKDIR /plane_task

# run the app
CMD [ "python", "app.py"]

# # incoming port
EXPOSE 5000

# # shell command
# CMD ["python3", "app.py"]
