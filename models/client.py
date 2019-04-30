from models.base_model import BaseModel
from models.user import User
import peewee as pw

class Client(BaseModel):
    name = pw.CharField(unique=True)
    industry = pw.CharField()
    country = pw.CharField()

    def validate(self):
        # new client validation (check for duplicates)
        duplicate_name = Client.get_or_none(Client.name == self.name)

        if duplicate_name and not duplicate_name.id == self.id:
            self.errors.append('Client already exists in system.')