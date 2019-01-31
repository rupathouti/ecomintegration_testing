from flask import Flask, jsonify, abort, make_response, request
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/ecommerce'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = 'apple'

db = SQLAlchemy(app)

from profiles_api import *
from customer_api import *

if __name__ == '__main__':
    app.run(debug=True)