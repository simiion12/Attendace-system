from flask import Blueprint, jsonify, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from functools import wraps
import jwt
from back.models.admins import Admin
from back.models.departments import Departments
from back import app
from back.models import db
import bcrypt
import uuid

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
        db.session.add(new_admin)
        db.session.commit()

        return jsonify({'message': 'User registered successfully!'}), 201
    return jsonify({'message': 'This is the registration page'}), 200