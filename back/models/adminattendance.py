from back.models import db_postgres as db


class admin_attendance(db.Model):
    attendance_id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('back.models.admin.admin_id'), nullable=False)
    attendance_date = db.Column(db.Date, nullable=False)

    @staticmethod
    def insert_admin_attendance(admin_id, attendance_date):
        attendance_id = admin_attendance.query.order_by(admin_attendance.attendance_id.desc()).first().attendance_id + 1
        new_admin_attendance = admin_attendance(attendance_id=attendance_id, admin_id=admin_id, attendance_date=attendance_date)
        db.session.add(new_admin_attendance)
        db.session.commit()

