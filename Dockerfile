FROM python:latest
COPY . /serverr/
RUN pip3 install -r ./serverr/requirements.txt
WORKDIR /serverr