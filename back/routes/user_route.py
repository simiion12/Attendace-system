from flask import Blueprint, jsonify, request, Response
from functools import wraps
import jwt
from back.models.users import Users
from back.models.departments import Departments
from back import app, mongo, grid_fs_users
from back.models import db_postgres as db
import gridfs
import bcrypt


# Create a Blueprint for the routes in this directory
user_routes = Blueprint("user_routes", __name__)

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
            current_user = Users.query.filter_by(user_id=data['user_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@user_routes.route('/user_register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        # Extract other form fields from the request parameters
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        department_id = request.form.get('department_id')

        if password != confirm:
            return jsonify({'message': 'Password and confirmation do not match'}), 400

        existing_user = Users.query.filter_by(username=username).first()

        existing_department = Departments.query.filter_by(department_id=department_id).first()
        if existing_user:
            return jsonify({'message': 'User already exists'}), 400
        if not existing_department:
            return jsonify({'message': 'Department does not exist'}), 400

        # Hashing the password
        pwhash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        pwhash = pwhash.decode('utf-8')

        #user_id = User.query.order_by(User.admin_id.desc()).first().admin_id + 1
        user_id = 1
        new_user = Users(user_id=user_id, username=username,password=pwhash,
                        full_name=full_name, email=email, department_id=department_id)

        # Adding photo in MongoDB
        file = request.files['file']
        file_id = grid_fs_users.put(file, filename=file.filename, user_id=user_id)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully with selfie photo', 'file_id': str(file_id)}), 201

    return jsonify({'message': 'This is the registration page'}), 200

@user_routes.route('/user_login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        valid_username, correct_password, face_recognized = False, False, False
        username = request.form.get('username')
        password = request.form.get('password')

        existing_user = Users.query.filter_by(username=username).first()
        if existing_user:
            valid_username = True
        else:
            return jsonify({'message': 'User does not exist'}), 400

        if bcrypt.checkpw(password.encode('utf-8'), existing_user.password.encode('utf-8')):
            correct_password = True
        else:
            return jsonify({'message': 'Password is incorrect'}), 400

        # Face recognition part
        photo_data_mongo = Users.face_retrieving(username)
        photo_data_new = request.files['file']
        if photo_data_mongo and photo_data_new:
            face_recognized = Users.face_recognition(photo_data_mongo, photo_data_new)

        if valid_username and correct_password and face_recognized:
            token = jwt.encode({'user_id': existing_user.user_id}, app.config['SECRET_KEY'])
            return jsonify({'token': token}), 200
        else:
            return jsonify({'message': 'Face not recognized'}), 400

    return jsonify({'message': 'This is the login page'}), 200
