from sqlalchemy import Column, Integer, String
from myflask.mysqlalchemy.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(50), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)


from marshmallow_sqlalchemy import ModelSchema
class UserScheme(ModelSchema):
    class Meta:
        model = User

user_scheme = UserScheme()
users_scheme = UserScheme(many=True)

