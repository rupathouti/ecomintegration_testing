from run import db, app, bcrypt
from functools import wraps
from datetime import datetime
from run import db, app, bcrypt
from flask import jsonify, abort, make_response, request
import jwt

class Users(db.Model):
    __tablename__ ='users'
    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(500))

# from customer_api import Users


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'Message': 'Token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            user = Users.query.filter_by(id=data['user_id']).first()
        except Exception as e:
            print(e)
            return jsonify({'Message': 'Token is Invalid'})

        return f(user, *args, **kwargs)

    return decorated


def get_token(user_id,email_id,password):
    d = {
        'user_id':user_id,
        'email_id':email_id,
        'password': password,
        'exp': datetime .datetime.utcnow()+datetime.timedelta(minutes=15)
        }
    token = jwt.encode(d, app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
    return token

@app.route('/register', methods=['POST'])
def register():

    data = request.get_json()
   
    user = Users.query.filter_by(email_id=data['email_id'])
    
    if user.count() == 0:
        pw_hash = bcrypt.generate_password_hash(data['password'])
        new_user = Users(email_id=data['email_id'],password=pw_hash)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Successfully registered'})
    else:
        return jsonify({'message': 'You are already registered or Please login using /login'})


@app.route('/login', methods=['POST'])
def login():

    data = request.get_json()
    
    user = Users.query.filter_by(email_id=data['email_id']).first()

    if user:
        flag = bcrypt.check_password_hash(user.password, data['password'])
        if flag:
            token = get_token(user.id,user.email_id,user.password)
            return jsonify({'token': token, 'message':'Successfully logged in'})
    
    return jsonify({'message': 'Invalid User...Please register using /register'})