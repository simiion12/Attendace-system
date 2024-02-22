from flask import Blueprint, jsonify, request, Response
from functools import wraps
import jwt
from back.models.admins import Admins
from back.models.departments import Departments
from back import app, mongo, grid_fs_admins
from back.models import db_postgres as db
import gridfs
import bcrypt
from back.models.users import Users
from back.models.admin_attendance import admin_attendance
from datetime import date

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
            current_admin = Admins.query.filter_by(admin_id=data['admin_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_admin, *args, **kwargs)

    return decorated


@admin_routes.route('/admin_register', methods=['GET', 'POST'])
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

        if secret_password != 'secret':
            return jsonify({'message': 'Secret password is incorrect'}), 400

        if admin_password != confirm:
            return jsonify({'message': 'Password and confirmation do not match'}), 400

        existing_admin = Admins.query.filter_by(username=admin_username).first()

        existing_department = Departments.query.filter_by(department_id=department_id).first()
        if existing_admin:
            return jsonify({'message': 'Admin already exists'}), 400
        if not existing_department:
            return jsonify({'message': 'Department does not exist'}), 400

        # Hashing the password
        pwhash = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())
        pwhash = pwhash.decode('utf-8')

        admin_id = Admins.query.order_by(Admins.admin_id.desc()).first().admin_id + 1
        #admin_id = 1
        new_admin = Admins(admin_id=admin_id, username=admin_username,
                          password=pwhash, full_name=admin_fullname,
                          email=admin_email, department_id=department_id)

        # Adding photo in MongoDB
        file = request.files['file']
        file_id = grid_fs_admins.put(file, filename=file.filename, admin_id=admin_id)

        db.session.add(new_admin)
        db.session.commit()

        return jsonify({'message': 'User registered successfully with selfie photo', 'file_id': str(file_id)}), 201

    return jsonify({'message': 'This is the registration page'}), 200


@admin_routes.route('/admin_login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        valid_username, correct_password, face_recognized = False, False, False
        admin_username = request.form.get('admin_username')
        admin_password = request.form.get('admin_password')

        existing_admin = Admins.query.filter_by(username=admin_username).first()
        if existing_admin:
            valid_username = True
        else:
            return jsonify({'message': 'Admin does not exist'}), 400

        if bcrypt.checkpw(admin_password.encode('utf-8'), existing_admin.password.encode('utf-8')):
            correct_password = True
        else:
            return jsonify({'message': 'Password is incorrect'}), 400

        # Face recognition part
        photo_data_mongo = Admins.face_retrieving(admin_username)
        photo_data_new = request.files['file']
        if photo_data_mongo and photo_data_new:
            face_recognized = Admins.face_recognition(photo_data_mongo, photo_data_new)

        if valid_username and correct_password and face_recognized:
            attendance_date = date.today()
            admin_attendance.insert_admin_attendance(existing_admin.admin_id, attendance_date)
            token = jwt.encode({'user_id': existing_admin.admin_id}, app.config['SECRET_KEY'])
            return jsonify({'token': token}), 200
        else:
            return jsonify({'message': 'Face not recognized'}), 400

    return jsonify({'message': 'This is the login page'}), 200

@admin_routes.route('/get_all_user_attendance', methods=['GET'])
def get_all_user_attendance():
    pass

@admin_routes.route('/get_all_admin_attendance', methods=['GET'])
def get_all_admin_attendance():
    pass

@admin_routes.route('/get_all_users', methods=['GET'])
def get_all_users():
    pass

@admin_routes.route('/get_all_admins', methods=['GET'])
def get_all_admins():
    pass

@admin_routes.route('/get_all_departments', methods=['GET'])
def get_all_departments():
    pass

@admin_routes.route('/get_userattendance_by_department', methods=['GET'])
def get_userattendance_by_department():
    pass

@admin_routes.route('/get_adminattendance_by_department', methods=['GET'])
def get_adminattendance_by_department():
    pass











"""@admin_routes.route('/post', methods=['POST'])
def postinmongo():
    admin_id = request.form['admin_id']
    file = request.files['file']

    # Create a GridFS instance for the admins_photos collection
    fs = gridfs.GridFS(mongo.db, collection='admins_photos')

    # Store the file in MongoDB using GridFS
    file_id = fs.put(file, filename=file.filename, admin_id=admin_id)

    return jsonify({'message': 'User registered successfully with selfie photo', 'file_id': str(file_id)}), 201


@app.route('/photo/<admin_id>', methods=['GET'])
def get_photo(admin_id):
    admin_id = int(admin_id)

    # Find the document in admins_photos.files collection
    photo_doc = mongo.db.admins_photos.files.find_one({'admin_id': admin_id})
    print("Retrieved document:", photo_doc)
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
    admins_photos_chunks = mongo.db.users_photos.chunks
    admins_photos_files = mongo.db.users_photos.files
    admins_photos_chunks.drop()
    admins_photos_files.drop()

    return jsonify({'message': 'All dropped'}), 200


@app.route('/all1', methods=['GET'])
def get_all1():
    # dropping all from postgres
    Users.query.delete()
    db.session.commit()
    return jsonify({'message': 'All dropped from postgres'}), 200

@app.route('/face', methods=['GET'])
def face():
    face_recognized = False
    photo_data_mongo = Admins.face_retrieving('panf')
    # file = request.files['file']
    photo_data_new = request.files['file']
    if photo_data_mongo and photo_data_new:
        face_recognized = Admins.face_recognition(photo_data_mongo, photo_data_new)
    return jsonify({'face_recognized': face_recognized}), 200"""