from app import db

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), index=True, nullable=False)
    module_code = db.Column(db.String(10), index=True, nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(1000), index=True)
    status = db.Column(db.Boolean, default=False)
