w## python 3
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

## relationship
jack = User('jack', 'Jack Bean', 'sadfjklas')
print('empty', jack.addresses) # [] 빈 리스트를 반환

jack.addresses = [
    Address(email_address='jack@gmail.com'),
    Address(email_address='jack@yahoo.com')
]

print('added', jack.addresses)

print(jack.addresses[1])
print(jack.addresses[1].user)

session.add(jack)
session.commit()

jack = session.query(User).filter_by(name='jack').one()
print(jack.id, jack)
print('lazy loading', jack.addresses)

## join
jacksEmail = session.query(User, Address).filter(User.id==Address.user_id).filter(Address.email_address=='jack@gmail.com').all()
print(jacksEmail)

jacksEmail = session.query(User).join(Address).filter(Address.email_address=='jack@gmail.com').all()
print(jacksEmail)

## 조인 조건
jacksEmail = session.query(User).join(Address, User.id==Address.user_id).filter(Address.email_address=='jack@gmail.com').all()
print(jacksEmail)

jacksEmail = session.query(User).join(User.addresses).filter(Address.email_address=='jack@gmail.com').all()
print(jacksEmail)

jacksEmail = session.query(User).join(Address, User.addresses).filter(Address.email_address=='jack@gmail.com').all()
print(jacksEmail)

jacksEmail = session.query(User).join('addresses').filter(Address.email_address=='jack@gmail.com').all()
print(jacksEmail)

## outer
jacksEmail = session.query(User).outerjoin(User.addresses).all()
print('outerjoin', jacksEmail)

from sqlalchemy import and_
jacksEmail = session.query(User).outerjoin(Address, and_(User.id == Address.user_id, Address.email_address=='jack@naver.com')).all()
print('outerjoin multiple condition', jacksEmail)

from sqlalchemy.orm import aliased
address_alias1 = aliased(Address)
address_alias2 = aliased(Address)

joined = session.query(User.name, address_alias1.email_address, address_alias2.email_address). \
    outerjoin(address_alias2, User.addresses). \
    join(address_alias1, User.addresses). \
    filter(address_alias1.email_address == 'jack@gmail.com').\
    filter(address_alias2.email_address == 'jack@yahoo.com').all()

print(joined)

## subquery
from sqlalchemy.sql import func
stmt = session.query(Address.user_id, func.count('*').label('address_count')).group_by(Address.user_id).subquery()
users = session.query(User, stmt.c.address_count).outerjoin(stmt, User.id==stmt.c.user_id).order_by(User.id).all()

print('subquery', users)

stmt = session.query(Address).filter(Address.email_address != 'jack@yahoo.com').subquery()
address_alias1 = aliased(Address, stmt)

users = session.query(User, address_alias1).join(address_alias1, User.addresses).all();
print('subquery aliased', users)

from sqlalchemy.sql import exists
stmt = exists().where(Address.user_id == User.id)
users = session.query(User.name).filter(stmt).all()
print('exists', users)

users = session.query(User.name).filter(User.addresses.any()).all()
print('any', users)

users = session.query(User.name).filter(User.addresses.any(Address.email_address.like('%jack%'))).all()
print('any condition', users)

users = session.query(User.name).filter(~User.addresses.any(Address.email_address.like('%jack%'))).all()
print('any NOT condition', users)

## eager loading
from sqlalchemy.orm import subqueryload
jack = session.query(User).options(subqueryload(User.addresses)).filter_by(name='jack').one()
print(jack)
print('eager loaded(subquery)', jack.addresses)

from sqlalchemy.orm import joinedload
jack = session.query(User).options(joinedload(User.addresses)).filter_by(name='jack').one()
# Address는 익명 alias로 참조되어서 Address에 대한 추가 조건을 설정 할 수 없다
print(jack)
print('eager loaded(outer join)', jack.addresses)

from sqlalchemy.orm import contains_eager
jack_addresses = session.query(Address).join(Address.user).filter(User.name == 'jack').\
    options(contains_eager(Address.user)).all()

print(jack_addresses)
print(jack_addresses[0].user)

## delete
jack = session.query(User).filter(User.name=='jack').one()
print('before delete', session.query(User).filter(User.name=='jack').count())
session.delete(jack)
print('deleted', session.query(User).filter(User.name=='jack').count())

print('remain addresses', session.query(Address).filter(Address.email_address.like('%jack%')).count())
### cascade add. class User
###     addresses = relationship("Address", backref='user', cascade="all, delete, delete-orphan")
