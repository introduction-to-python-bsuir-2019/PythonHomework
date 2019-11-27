FROM python:3.8

RUN mkdir /code

WORKDIR /code

ADD requirements.txt code/requirements.txt
ADD README.md code/README.md
ADD setup.py code/setup.py

RUN cd code