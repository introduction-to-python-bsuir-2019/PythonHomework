FROM python:3.8

RUN mkdir /code

WORKDIR /code
ADD . /code
ADD requirements.txt code/requirements.txt

RUN python3.8 -m pip install --upgrade -r requirements.txt
ENV PYTHONPATH "${PATHONPATH}:/rssreader"