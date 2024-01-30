from back.models import db


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_username = db.Column(db.String(100), nullable=False)
    user_password_hash = db.Column(db.String(100), nullable=False)
    user_fullname = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('back.models.department.department_id'), nullable=False)