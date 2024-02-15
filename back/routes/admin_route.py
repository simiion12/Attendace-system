from flask import Blueprint, jsonify, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from functools import wraps
import jwt
from back.models.admins import Admins
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
            current_admin = Admins.query.filter_by(user_ID=data['user_ID']).first()
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
    department_id = StringField('Department ID', validators=[DataRequired()])


@admin_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        secret_password = request.form.get('secret_password')
        print(secret_password)
        if secret_password != 'secret':
            return jsonify({'message': 'Secret password is incorrect'}), 400

        # Extract other form fields from the request parameters
        admin_username = request.form.get('admin_username')
        admin_password = request.form.get('admin_password')
        confirm = request.form.get('confirm')
        admin_fullname = request.form.get('admin_fullname')
        admin_email = request.form.get('admin_email')
        department_id = request.form.get('department_id')

        #form = RegistrationForm()
        #if not form.validate():
          #  return jsonify({'message': 'Invalid form', 'errors': form.errors}), 400

        if secret_password != 'secret':
            return jsonify({'message': 'Secret password is incorrect'}), 400

        if admin_password != confirm:
            return jsonify({'message': 'Password and confirmation do not match'}), 400

        #existing_admin = Admins.query.filter_by(admin_username=admin_username).first()

        existing_department = Departments.query.filter_by(department_id=department_id).first()
        #if existing_admin:
        #    return jsonify({'message': 'Admin already exists'}), 400
        if not existing_department:
            return jsonify({'message': 'Department does not exist'}), 400

        # Hashing the password
        pwhash = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())
        pwhash = pwhash.decode('utf-8')

        #admin_id = uuid.uuid4()
        admin_id = 1
        new_admin = Admins(admin_id=admin_id, username=admin_username,
                          password=pwhash, full_name=admin_fullname,
                          email=admin_email, department_id=department_id)

        # Adding photo in MongoDB
        file = request.files['file']
        fs = gridfs.GridFS(mongo.db, collection='admins_photos')
        file_id = fs.put(file, filename=file.filename, admin_id=admin_id)

        db.session.add(new_admin)
        db.session.commit()

        return jsonify({'message': 'User registered successfully with selfie photo', 'file_id': str(file_id)}), 201

    return jsonify({'message': 'This is the registration page'}), 200


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
    # dropping all
    admins_photos_chunks = mongo.db.admins_photos.chunks
    admins_photos_files = mongo.db.admins_photos.files
    admins_photos_chunks.drop()
    admins_photos_files.drop()

    return jsonify({'message': 'All dropped'}), 200


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

