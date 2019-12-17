FROM python:3.8-alpine3.10

LABEL Author='Andrei Puzanau'
LABEL version="0.1"

WORKDIR /app
COPY rssreader ./rssreader/
COPY webapi ./webapi/
COPY setup.py .

RUN pip install .

EXPOSE 5000
ENV FLASK_APP webapi.webapp.py
CMD flask run --host=0.0.0.0
