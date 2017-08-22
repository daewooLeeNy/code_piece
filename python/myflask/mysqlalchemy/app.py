from flask import Flask, jsonify
from flask_restful import Api, reqparse

from myflask.mysqlalchemy.database import db_session
from myflask.mysqlalchemy.models import User, user_scheme, users_scheme

app = Flask(__name__)
api = Api(app)
## DB 생성이 필요한 경우 database.init_db()를 별도로(cmd) 호출 하여 생성 한다.
## from myflask.mysqlalchemy.database import init_db
## init_db();

@app.route("/")
def hello():
    return "Hello!"

@app.route("/users", methods=['GET'])
def users():
    result = db_session.query(User).all();
    return jsonify(users_scheme.dump(result))


@app.route("/users/<id>", methods=['GET'])
def user(id):
    result = db_session.query(User).filter(User.id == id).one();
    return jsonify(user_scheme.dump(result))


parser = reqparse.RequestParser()
parser.add_argument('userName', required=True,type=str, help='사용자 명칭')
parser.add_argument('email', required=True, type=str, help='email')

@app.route("/users", methods=['POST'])
def register():
    args = parser.parse_args();
    user = User()
    user.name = args['userName']
    user.email = args['email']

    db_session.add(user)
    try:
        db_session.commit()
    except:
        return "", 409

    return "SUCCESS"

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(debug=True)
