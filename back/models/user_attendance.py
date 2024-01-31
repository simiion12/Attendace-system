from back.models import db


class UserAttendance(db.Model):
    user_attendance_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('back.models.user.user_id'), nullable=False)
    attendance_date = db.Column(db.Date, nullable=False)
