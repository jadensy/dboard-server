from models.base_model import BaseModel
import peewee as pw

class Project(BaseModel):
    name = pw.CharField()
    type = pw.CharField()
    client_id = pw.ForeignKeyField(Client, backref='projects')
    date = pw.DateField()
    currency = pw.CharField()
    total = pw.DecimalField()