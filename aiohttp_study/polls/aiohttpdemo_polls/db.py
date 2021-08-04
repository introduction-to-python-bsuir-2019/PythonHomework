'''
Start from:
Run Postgres:
    docker run --rm -it -p 5432:5432 postgres:10
or in my case:
    docker run --rm -it -p 5432:5432 postgres:12.0-alpine

Then create DB, role and rights:

$ psql -U postgres -h localhost
> CREATE DATABASE aiohttpdemo_polls;
> CREATE USER aiohttpdemo_user WITH PASSWORD 'aiohttpdemo_pass';
> GRANT ALL PRIVILEGES ON DATABASE aiohttpdemo_polls TO aiohttpdemo_user;
'''
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, Date
)

meta = MetaData()

question = Table(
    'question', meta,

    Column('id', Integer, primary_key=True),
    Column('question_text', String(200), nullable=False),
    Column('pub_date', Date, nullable=False)
)

choice = Table(
    'choice', meta,

    Column('id', Integer, primary_key=True),
    Column('choice_text', String(200), nullable=False),
    Column('votes', Integer, server_default="0", nullable=False),

    Column('question_id',
           Integer,
           ForeignKey('question.id', ondelete='CASCADE'))
)
