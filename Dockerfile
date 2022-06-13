FROM alpine
RUN apk update
RUN apk install vim
RUN apk install net-tools

FROM python:3

COPY . /app
WORKDIR /app



RUN pip3 install --no-cache-dir --upgrade  -r requirements.txt

