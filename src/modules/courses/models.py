from src.service_modules.db.conn import db

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80),nullable=False)
    category = db.Column(db.String(80),nullable=False)
    description = db.Column(db.String(256), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    instructor_name = db.Column(db.String(80),nullable=False)
    language = db.Column(db.String(80),nullable=False)
    level = db.Column(db.String(80),nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(80),nullable=False)
    visibility = db.Column(db.String(80),nullable=False)
    chapters = db.relationship('Chapter', backref = 'course')
    quizzes = db.relationship('Quizz', backref = 'course')

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80),nullable=False)
    content = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    videoLink = db.Column(db.String(256),nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))