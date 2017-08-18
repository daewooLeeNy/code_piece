## (De)Serialize to json
## http://www.haruair.com/blog/1695
## python 3
import sqlalchemy
from sqlalchemy import create_engine

print(sqlalchemy.__version__)
engine = create_engine('sqlite:///:memory:', echo=True)

print(engine.execute("select 1").scalar())

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
## engine을 나중에 설정 하는 방법
##Session = sessionmaker()
##Session.configure(bind=engine)

session = Session()

from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))
    addresses = relationship("Address", order_by="Address.id", backref="user")
    ## casecade
    #addresses = relationship("Address", backref='user', cascade="all, delete, delete-orphan")
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return "<User('%s, '%s', '%s')>" % (self.name, self.fullname, self.password)


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    # user = relationship("User", backref=backref('addresses', order_by=id))
    def __init__(self, email_address):
        self.email_address = email_address

    def __repr__(self):
        return "<Address('%s')>" % self.email_address

Base.metadata.create_all(engine)

## https://marshmallow-sqlalchemy.readthedocs.io/en/latest/
## serialize to json
from marshmallow_sqlalchemy import ModelSchema
class UserScheme(ModelSchema):
    class Meta:
        model = User

class AddressScheme(ModelSchema):
    class Meta:
        model = Address

user_scheme = UserScheme()

jack = User('jack', 'Jack Bean', 'sadfjklas')
jack.addresses = [
    Address(email_address='jack@gmail.com'),
    Address(email_address='jack@yahoo.com')
]
session.add(jack)
session.commit()

dump_data = user_scheme.dump(jack).data
print('serialize', dump_data)

de_user = user_scheme.load(dump_data, session=session).data
print('deserialize', de_user)


## collection serialize
john = User('john', 'John', 'test')
session.add(john)
session.commit()

result = session.query(User).all()
dump_datas = user_scheme.dump(result, many=True).data

print('collection serialize', dump_datas)

de_users = []
for d in dump_datas:
    de = user_scheme.load(d, session=session).data
    de_users.append(de)

print('collection deserialize', de_users)