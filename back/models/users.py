from back.models import db_postgres as db
import face_recognition
from back import mongo, grid_fs_users
from flask import jsonify

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'), nullable=False)

    @staticmethod
    def face_retrieving(username):
        user_id = Users.query.filter_by(username=username).first().user_id
        user_photo = mongo.db.users_photos.files.find_one({'user_id': user_id})
        if user_photo:
            file_id = user_photo['_id']
            # Retrieve the file content using the file_id from GridFS
            file_data = grid_fs_users.get(file_id)

            if file_data:
                return file_data
            else:
                return jsonify({'message': 'No photo found for admin_id {}'.format(user_id)}), 404
        else:
            return jsonify({'message': 'No photo found for admin_id {}'.format(user_id)}), 404

    @staticmethod
    def face_recognition(photo_data_mongo, photo_data_new):
        # Convert the photo data to an array
        photo_array_mongo = face_recognition.load_image_file(photo_data_mongo)
        photo_array_new = face_recognition.load_image_file(photo_data_new)

        # Find face encodings for each photo
        face_encodings1 = face_recognition.face_encodings(photo_array_mongo)
        face_encodings2 = face_recognition.face_encodings(photo_array_new)

        # Compare face encodings
        if face_encodings1 and face_encodings2:
            match = face_recognition.compare_faces([face_encodings1[0]], face_encodings2[0])
            if match[0]:
                return True
            else:
                return False


