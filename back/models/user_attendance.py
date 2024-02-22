from back.models import db_postgres as db


class user_attendance(db.Model):
    attendance_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    attendance_date = db.Column(db.Date, nullable=False)

    @staticmethod
    def insert_user_attendance(user_id, attendance_date):
        attendance_id = user_attendance.query.count() + 1

        new_user_attendance = user_attendance(attendance_id=attendance_id, user_id=user_id, attendance_date=attendance_date)
        db.session.add(new_user_attendance)
        db.session.commit()