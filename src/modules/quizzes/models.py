from src.service_modules.db.conn import db

class Quizz(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    status = db.Column(db.String(80),nullable=False)
    questions = db.relationship('Question', backref = 'quizz')

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.String(256), nullable=False)
    options = db.Column(db.String(256), nullable=False)
    answer = db.Column(db.String(256), nullable=False)
    quizz_id = db.Column(db.Integer, db.ForeignKey('quizz.id'))