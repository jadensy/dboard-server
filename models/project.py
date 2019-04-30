from models.base_model import BaseModel
from models.client import Client
import peewee as pw

class Project(BaseModel):
    name = pw.CharField()
    project_type = pw.CharField()
    client_id = pw.ForeignKeyField(Client, backref='projects')
    date = pw.DateField()
    currency = pw.CharField()
    total = pw.DecimalField(decimal_places=2)