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
            current_user = User.query.filter_by(user_id=data['user_id']).first()
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
