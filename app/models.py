from app import db
class Task(db.Model):
    id = db.column(db.Integer, primary_key = True)
    title = db.column(db.String(100), nullable = False)
    ststus = db.column(db.String(20), default = "Pending")