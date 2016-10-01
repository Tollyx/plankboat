import peewee

db = peewee.SqliteDatabase('plankboat.db')

class BaseModel(peewee.Model):
    class Meta:
        database = db

db.connect()

def getDB():
    return db

def close()
    db.close()