from back.models import db_postgres as db


class admin_attendance(db.Model):
    attendance_id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.admin_id'), nullable=False)
    attendance_date = db.Column(db.Date, nullable=False)

    @staticmethod
    def insert_admin_attendance(admin_id, attendance_date):
        attendance_id = admin_attendance.query.count() + 1
        new_admin_attendance = admin_attendance(attendance_id=attendance_id, admin_id=admin_id, attendance_date=attendance_date)
        db.session.add(new_admin_attendance)
        db.session.commit()

