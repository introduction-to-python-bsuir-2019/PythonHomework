FROM python:3.8

RUN mkdir /code

WORKDIR /code

ADD app/saved_files code/app/saved_files
ADD requirements.txt code/requirements.txt
ADD app/__init__.py code/app/__init__.py
ADD app/core.py code/app/core.py
ADD README.md code/README.md
ADD setup.py code/setup.py
RUN cd code; python3.8 setup.py install

