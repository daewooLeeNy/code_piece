## http://www.haruair.com/blog/1682
## python 3

import sqlalchemy
from sqlalchemy import create_engine

print(sqlalchemy.__version__)
engine = create_engine('sqlite:///:memory:', echo=True)

print(engine.execute("select 1").scalar())

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String, Sequence

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return "<User('%s, '%s', '%s')>" % (self.name, self.fullname, self.password)

print(User.__table__)
print(User.__mapper__)

Base.metadata.create_all(engine)

ed_user = User('lsinji', 'lsinji_full', '1234')
print(ed_user.name)
print(ed_user.fullname)
print(ed_user.password)
print(ed_user)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
## engine을 나중에 설정 하는 방법
##Session = sessionmaker()
##Session.configure(bind=engine)

session = Session()

## basic transaction
print('user_id %s' % ed_user.id)
session.add(ed_user)
session.commit();
print('after commit. user_id %s' % ed_user.id)

ed_user.name = 'lsinji_change';

fake_user = User('fakeuser', 'Invalid', '12345')
session.add(fake_user)

print(session.query(User).filter(User.name.in_(['lsinji_change', 'fakeuser'])).all())
session.rollback();

print(ed_user.name)
print(fake_user in session)

session.add(fake_user)
session.commit();

## basic query
for instance in session.query(User).order_by(User.id):
    print(instance.name, instance.fullname)

for row in session.query(User, User.name).all():
    print(row.User, row.name)

for row in session.query(User.name.label('name_label')).all():
    print(row.name_label)

from sqlalchemy.orm import aliased
user_alias = aliased(User, name='user_alias')

for row in session.query(user_alias, user_alias.name).all():
    print(row.user_alias)

for user in session.query(User).order_by(User.id)[0:1]:
    print(user)

for name in session.query(User).filter_by(name='fakeuser'):
    print(name)

for name in session.query(User).filter(User.name.like('%user%')):
    print(name)

for name in session.query(User).filter(User.name.contains('user')):
    print(name)

## list
query = session.query(User).order_by(User.id)
print(query.all())
print(query.first())

print('one()', query.filter(User.name == 'lsinji').one())

## except
from sqlalchemy.orm.exc import MultipleResultsFound
try:
    user = query.one()
except MultipleResultsFound as e:
    print(e)

from sqlalchemy.orm.exc import NoResultFound
try:
    user = query.filter(User.id == 99).one()
except NoResultFound as e:
    print(e)


## query string
## The text() construct is used to compose a textual statement.
## http://docs.sqlalchemy.org/en/latest/core/tutorial.html#using-textual-sql
from sqlalchemy.sql import text
query = session.query(User).filter(text('id<224')).order_by('id')
print('string query', query.all())

## bind
_one = session.query(User).filter(text('id<:value and name=:name')).params(value=1234, name='lsinji').order_by(User.id).one()
print('bind value', _one)

## statement
_list = session.query(User).from_statement(text('SELECT * FROM users WHERE name=:name')).params(name='lsinji').all()
print(_list)


## string SQL or Model
from sqlalchemy import func
from sqlalchemy.sql import desc
session.add_all([User('Jim', 'Stewart', 12345)])
ua = aliased(User)
query = session.query(User).from_self(User.id, User.name, ua.name).\
    filter(User.name < ua.name).\
    filter(func.length(ua.name) != func.length(User.name))

print('string', query.order_by('name').all())

print('model', query.order_by(desc(ua.name)).all())

print(session.query(User).filter(User.name.like('lsi%')).count())

print(session.query(func.count(User.name), User.name).group_by(User.name).all())

print(session.query(func.count('*')).select_from(User).scalar())
print(session.query(func.count(User.id)).scalar())
