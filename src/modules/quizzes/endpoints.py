from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint
from http import HTTPStatus
from sqlalchemy import and_
from marshmallow import ValidationError
from src.service_modules.db.conn import db
from src.modules.quizzes.models import Quizz, Question
from src.modules.courses.models import Course
from src.modules.quizzes.parameter import Post_req, Res_req
from src.modules.quizzes.response import QuizzResponse
from src.utils.helper import handle_error

api = Blueprint("Quizzes",__name__,description="Operations on Quizzes")

@api.route('/api/courses/<course_id>/quizzes/page/<num>')
class GettingQuizzes(MethodView):

    @api.response(HTTPStatus.OK,schema=QuizzResponse(many=True))
    def get(self, course_id, num):
        try:
            if num.isdigit():
                page = int(num)
                per_page = 10
            else:
                raise Exception("Invalid page number.", HTTPStatus.BAD_REQUEST)
            
            res = Quizz.query.filter(and_(Quizz.course_id == course_id, Quizz.status == 'active')).paginate(page=page, per_page=per_page)
            
            if res == []:
                raise Exception("There is no Quizzes with this Course id.", HTTPStatus.NOT_FOUND)
            
            return res
        
        except Exception as e:
            abort(handle_error(e))

@api.route('/api/courses/<course_id>/quizzes')
class QuizzOperations(MethodView):

    @api.arguments(schema=Post_req())
    def post(self, req_data, course_id):
        try:
            course = Course.query.filter(and_(Course.id == course_id, Course.status == 'published', Course.visibility == "public")).first()
            if course == None:
                raise Exception("The Course id is not listed", HTTPStatus.NOT_FOUND)
            entry = Quizz(course = course, status = "active")
            NewQuestions = req_data.get('questions')
            for question in NewQuestions:
                entry1 = Question(question = question.get('question'), options = str(question.get('options')), answer = question.get('answer'), quizz = entry)
                db.session.add(entry1)
            db.session.add(entry)
            db.session.commit()
            return {"message":"Quizz added successfully to the Course.","status": HTTPStatus.OK}
        
        except Exception as e:
            abort(handle_error(e))


@api.route('/api/quizzes/<id>')
class QuizzOperationsID(MethodView):

    @api.response(HTTPStatus.OK,schema=QuizzResponse())
    def get(self, id):
        try:
            res = Quizz.query.filter(and_(Quizz.id == id, Quizz.status == 'active')).first()
            if res == None:
                raise Exception("The Quizz id is not listed", HTTPStatus.NOT_FOUND)
            
            return res
        
        except Exception as e:
            abort(handle_error(e))

    @api.arguments(schema=Post_req())
    def put(self, req_data, id):
        try:
            res = Quizz.query.filter(and_(Quizz.id == id, Quizz.status == 'active')).first()

            if res == None:
                raise Exception("The Quizz id is not listed", HTTPStatus.NOT_FOUND)
            
            NewQuestions = req_data.get('questions')
            for question in NewQuestions:
                entry = Question(question = question.get('question'), options = str(question.get('options')), answer = question.get('answer'), quizz = res)
                db.session.add(entry)
            db.session.commit()
            return {"message":"Quizzes added successfully to the Course.","status": HTTPStatus.OK}
        
        except Exception as e:
            abort(handle_error(e))

    def delete(self,id):
        try:
            res = Quizz.query.filter_by(id=id).first()

            if res == None:
                raise Exception("The Quizz id is not listed", HTTPStatus.NOT_FOUND)

            res.status = "deleted"
            db.session.commit()

            return {'message':'Quizz successfully Deleted',"status": HTTPStatus.OK}
        
        except Exception as e:
            abort(handle_error(e))

@api.route('/api/quizzes/<id>/result')
class QuizzResult(MethodView):

    @api.arguments(schema=Res_req())
    def post(self, req_data, id):
        try:
            res = Quizz.query.filter(and_(Quizz.id == id, Quizz.status == 'active')).first()
            if res == None:
                    raise Exception("The Quizz id is not listed", HTTPStatus.NOT_FOUND)
            questions = res.questions
            answers = req_data.get("answers")
            marks = 0

            for answer in answers:
                for question in questions:
                    if answer['question_id'] == question.id and answer['answer'] == question.answer:
                        marks += 2
                        break
            return {'message':f'You Scored: {marks}',"status": HTTPStatus.OK}
        
        except Exception as e:
            abort(handle_error(e))



@api.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return {e.messages, HTTPStatus.BAD_REQUEST}
