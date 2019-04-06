import datetime

from peewee import *
from playhouse.sqlite_ext import JSONField

from api import db_path


db = SqliteDatabase(db_path)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    name = TextField()
    tz = CharField(max_length=10, primary_key=True)
    username = TextField()
    passw = TextField()


class Course(BaseModel):
    name = TextField()
    number = BigIntegerField(primary_key=True)
    prequisits = TextField()
    points = DoubleField(null=True)
    

class Faculty(BaseModel):
    name = TextField(primary_key=True)
    nums = TextField()


def initialize_db():
    db.connect()
    db.create_tables([Faculty, Course, User], safe=True)
    db.close()


if __name__ == '__main__':
    initialize_db()  # if db tables are not created, create them