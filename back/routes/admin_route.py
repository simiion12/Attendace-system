from flask import Blueprint, jsonify, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from functools import wraps
import jwt
from back.models.admins import Admin
from back.models.admins_photos import AdminsPhoto
from back.models.departments import Departments
from back import app, grid_fs
from back.models import db_postgres as db
from back import mongo
import gridfs
import bcrypt
import uuid
import os
from werkzeug.utils import secure_filename


# Create a Blueprint for the routes in this directory
admin_routes = Blueprint("admin_routes", __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        print(request.headers)
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_admin = Admin.query.filter_by(user_ID=data['user_ID']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_admin, *args, **kwargs)

    return decorated
class RegistrationForm(FlaskForm):
    secret_password = PasswordField('Secret Password', validators=[DataRequired()])
    admin_username = StringField('Username', validators=[DataRequired()])
    admin_password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    admin_fullname = StringField('Fullname', validators=[DataRequired()])
    admin_email = StringField('Email', validators=[DataRequired(), Email()])
   # department_id = StringField('Department ID', validators=[DataRequired()])


@admin_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        form = RegistrationForm()

        if form.secret_password != 'secret':
            return jsonify({'message': 'Secret password is incorrect'}), 400

        if form.admin_password != form.confirm:
            return jsonify({'message': 'Password and confirmation do not match'}), 400

        existing_admin = Admin.query.filter_by(admin_username=form.admin_username).first()
        existing_department = Departments.query.filter_by(department_id=form.department_id).first()
        if existing_admin:
            return jsonify({'message': 'Admin already exists'}), 400
        if not existing_department:
            return jsonify({'message': 'Department does not exist'}), 400


        # Hashing the password
        pwhash = bcrypt.hashpw(form.admin_password.encode('utf-8'), bcrypt.gensalt())
        pwhash = pwhash.decode('utf-8')
        #print(pwhash)
        admin_id = uuid.uuid4()
        print(admin_id)
        new_admin = Admin(admin_id=admin_id, admin_username=form.admin_username, admin_password_hash=pwhash, admin_fullname=form.admin_fullname, admin_email=form.admin_email)

        # Adding photo in mongoDB



        db.session.add(new_admin)
        db.session.commit()

        return jsonify({'message': 'User registered successfully!'}), 201
    return jsonify({'message': 'This is the registration page'}), 200

@admin_routes.route('/registerphoto', methods=['POST'])
def register_with_photo():
    # Check if the request contains a file
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400

    admin_id = request.form['admin_id']
    file = request.files['file']

    # Save the file directly to MongoDB using PyMongo
    file_id = mongo.save_file(file.filename, file)

    # Now you can proceed with user registration along with the file_id stored in MongoDB

    # Example: Saving the user details along with the file_id in the database
    new_admin_photo = AdminsPhoto(admin_id=admin_id, admin_photo=file_id)
    new_admin_photo.save()

    return jsonify({'message': 'User registered successfully with selfie photo'}), 201

@admin_routes.route('/post', methods=['POST'])
def postinmongo():
    admin_id = request.form['admin_id']
    file = request.files['file']

    # Create a GridFS instance for the admins_photos collection
    fs = gridfs.GridFS(mongo.db, collection='admins_photos')

    # Store the file in MongoDB using GridFS
    file_id = fs.put(file, filename=file.filename, admin_id=admin_id)

    return jsonify({'message': 'User registered successfully with selfie photo', 'file_id': str(file_id)}), 201
@app.route('/photos/<admin_id>', methods=['GET'])
def get_photos(admin_id):
    # Query the admins_photos collection to get the file_id associated with the admin_id
    admin_photo = mongo.db.admins_photos.files.find_one({'admin_id': admin_id})
    if admin_photo:
        file_id = admin_photo['_id']
        # Retrieve the file content using the file_id from GridFS
        file_data = grid_fs.get(file_id)
        # Return the file content
        return jsonify({'admin_id': admin_id, 'file_data': file_data.read().decode('utf-8')}), 200
    else:
        return jsonify({'message': 'No photo found for admin_id {}'.format(admin_id)}), 404

from flask import Response

@app.route('/photo/<admin_id>', methods=['GET'])
def get_photo(admin_id):
    # Find the document in admins_photos.files collection
    photo_doc = mongo.db.admins_photos.files.find_one({'admin_id': admin_id})

    if photo_doc:
        # Get the file_id from the photo document
        file_id = photo_doc['_id']

        # Find the corresponding data in admins_photos.chunks collection
        data_chunk = mongo.db.admins_photos.chunks.find_one({'files_id': file_id})

        if data_chunk:
            # Extract the binary data
            binary_data = data_chunk['data']

            # Set the appropriate Content-Type header for the response
            headers = {'Content-Type': 'image/jpeg'}

            # Return the binary data as a response
            return Response(binary_data, headers=headers)
        else:
            return jsonify({'message': 'Photo data not found'}), 404
    else:
        return jsonify({'message': 'Photo not found'}), 404



@app.route('/all', methods=['GET'])
def get_all():

    fs = gridfs.GridFS(mongo.db, collection='admins_photos.chunks')
    admin_photos = fs.find()
    for admin_photo in admin_photos:
        if admin_photo is not None:
            print(admin_photo)
    print(admin_photos)

    return jsonify({admin_photos}), 200


