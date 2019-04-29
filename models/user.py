from models.base_model import BaseModel
import peewee as pw

class User(BaseModel):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField()

    def validate(self):
        # new user validation (check for duplicates)
        duplicate_username = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)

        if duplicate_username and not duplicate_username.id == self.id:
            self.errors.append('Username has been registered. Please try another.')
        elif duplicate_email and not duplicate_email.id == self.id:
            self.errors.append('Email has been registered. Please try another.')

