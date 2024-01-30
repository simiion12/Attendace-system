from back.models import db


class AdminAttendance(db.Model):
    admin_attendance_id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('back.models.admin.admin_id'), nullable=False)
    attendance_date = db.Column(db.Date, nullable=False)


