from myflask.mysqlalchemy.database import db_session, init_db
from myflask.mysqlalchemy.models import User

init_db()

u = User('admin', 'admin@localhost')
db_session.add(u)
db_session.commit()

print(User.query.all())