from back.models import db_postgres
from flask import Flask
from mongoengine import connect
from flask_pymongo import PyMongo
from gridfs import GridFS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/postgres'
app.config['MONGO_DBNAME'] = 'Attendance'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Attendance'

connect(db='Attendance', host='mongodb://localhost:27017/Attendance')
#client = pymongo.MongoClient("mongodb://localhost:27017/flask_db")
# Initialize the SQLAlchemy, Mongo database
db_postgres.init_app(app)
mongo = PyMongo(app)

grid_fs_admins = GridFS(mongo.db, collection='admins_photos')
grid_fs_users = GridFS(mongo.db, collection='users_photos')
