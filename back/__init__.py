from back.models import db
from flask import Flask
from mongoengine import connect
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/postgres'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/flask_db'

connect(db='Attendance', host='mongodb://localhost:27017/flask_db')

# Initialize the SQLAlchemy database
db.init_app(app)