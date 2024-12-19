from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint
from http import HTTPStatus
from marshmallow import ValidationError
from sqlalchemy import and_
from src.service_modules.db.conn import db
from src.modules.courses.models import Course, Chapter
from src.modules.courses.parameter import Post_req, Put_req
from src.modules.courses.response import CourseResponse
from src.utils.helper import handle_error

api = Blueprint("Courses",__name__,description="Operations on Courses")

@api.route('/api/courses/page/<num>')
class GettingCourses(MethodView):

    @api.response(HTTPStatus.OK,schema=CourseResponse(many=True))
    def get(self,num):
        try:
            if num.isdigit():
                page = int(num)
                per_page = 10
            else:
                raise Exception("Invalid page number.", HTTPStatus.BAD_REQUEST)
            
            res = Course.query.filter(and_(Course.status == "published", Course.visibility == "public")).paginate(page=page, per_page=per_page)
            if res == None:
                raise Exception("The are no Courses", HTTPStatus.NOT_FOUND)

            return res
        
        except Exception as e:
            abort(handle_error(e))

@api.route('/api/courses')
class CourseOperations(MethodView):

    @api.arguments(schema=Post_req())
    def post(self, req_data):
        try:
            entry = Course(title = req_data.get('title'), category = req_data.get('category'), description = req_data.get('description'), duration = req_data.get('duration'), instructor_name = req_data.get('instructor_name'), language = req_data.get('language'), level = req_data.get('level'), price = req_data.get('price'), status = req_data.get('status'), visibility = req_data.get('visibility'))
            Newchapters = req_data.get('chapters')
            for chapter in Newchapters:
                entry1 = Chapter(title = chapter.get('title'), content = chapter.get('content'), description = chapter.get('description'), videoLink = chapter.get('videoLink'), duration = chapter.get('duration'), course = entry)
                db.session.add(entry1)
            db.session.add(entry)
            db.session.commit()
            return {"message":"Course added successfully.","status": HTTPStatus.OK}
        
        except Exception as e:
            abort(handle_error(e))

@api.route('/api/courses/<id>')
class CourseOperationsID(MethodView):

    @api.response(HTTPStatus.OK,schema=CourseResponse())
    def get(self,id):
        try:
            res = Course.query.filter(and_(Course.id == id, Course.status == "published", Course.visibility == "public")).first()
            if res == None:
                raise Exception("The Course id is not listed", HTTPStatus.NOT_FOUND)
            
            return res
        
        except Exception as e:
            abort(handle_error(e))

    @api.arguments(schema=Put_req())
    def put(self,req_data, id):
        try:
            res = Course.query.filter(and_(Course.id == id, Course.status == "published", Course.visibility == "public")).first()

            if res == None:
                raise Exception("The Course id is not listed", HTTPStatus.NOT_FOUND)

            Newchapters = req_data.get('chapters')
            for chapter in Newchapters:
                entry = Chapter(title = chapter.get('title'), content = chapter.get('content'), description = chapter.get('description'), videoLink = chapter.get('videoLink'), duration = chapter.get('duration'), course = res)
                db.session.add(entry)
            db.session.commit()
            return {"message":"Chapter added to the course successfully.","status": HTTPStatus.OK}
        
        except Exception as e:
            abort(handle_error(e))
 
    def delete(self, id):
        try:
            res = Course.query.filter(and_(Course.id == id, Course.status == "published")).first()

            if res == None:
                raise Exception("The Course id is not listed", HTTPStatus.NOT_FOUND)

            res.status = "Deleted"
            db.session.commit()

            return {'message':'Course successfully Deleted',"status": HTTPStatus.OK}
        
        except Exception as e:
            abort(handle_error(e))

@api.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return {e.messages, HTTPStatus.BAD_REQUEST}