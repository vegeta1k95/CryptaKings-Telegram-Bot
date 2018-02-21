from peewee import *

db = SqliteDatabase('users.db')

class User(Model):
    user_id = CharField()
    first_name = CharField()
    last_name = CharField()
    password_hash = CharField()
    logged_in = BooleanField()

    class Meta:
        database = db
