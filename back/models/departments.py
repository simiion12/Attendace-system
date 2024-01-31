from back.models import db


class Departments(db.Model):
    department_id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(100), nullable=False)


def insert_department(id, department_name):
    new_department = Departments(department_id=id, department_name=department_name)
    db.session.add(new_department)
    db.session.commit()
