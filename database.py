import peewee

db = peewee.SqliteDatabase('plankboat.db')

class BaseModel(peewee.Model):
    class Meta:
        database = db

db.connect()

def close():
    db.close()
