from flask import Blueprint, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from back.models.departments import Departments
from back.models import db


# Create a Blueprint for the routes in this directory
department_routes = Blueprint("department_routes", __name__)

class DepartmentForm(FlaskForm):
    department_name = StringField('Department Name', validators=[DataRequired()])


@department_routes.route('/insert_department', methods=['GET', 'POST'])
def insert_department():
    if request.method == 'POST':
        department_name = request.form.get('department_name')
        if department_name:
            department_id = Departments.query.order_by(Departments.department_id.desc()).first().department_id + 1
            new_department = Departments(department_id=department_id, department_name=department_name)
            db.session.add(new_department)
            db.session.commit()

            return jsonify({'message': 'Department added successfully'}), 200
        else:
            return jsonify({'error': 'Department name is required'}), 400
    elif request.method == 'GET':
        return "This route only accepts POST requests."



