from back.models import db_postgres as db


class Admin(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    admin_username = db.Column(db.String(100), nullable=False)
    admin_password_hash = db.Column(db.String(100), nullable=False)
    admin_fullname = db.Column(db.String(100), nullable=False)
    admin_email = db.Column(db.String(100), nullable=False)
    #department_id = db.Column(db.Integer, db.ForeignKey('back.models.department.department_id'), nullable=False)
