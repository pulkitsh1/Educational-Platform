from flask import abort, Response
from flask.views import MethodView
from flask_smorest import Blueprint
import logging, json
from http import HTTPStatus
from marshmallow import ValidationError
from sqlalchemy import and_
from src.service_modules.db.conn import db
from src.modules.courses.models import Course, Chapter
from src.modules.courses.parameter import Post_req, Put_req
from src.modules.courses.response import CourseResponse

api = Blueprint("Courses",__name__,description="Operations on Courses")

@api.route('/api/courses')
class CourseOperations(MethodView):

    @api.response(HTTPStatus.OK,schema=CourseResponse(many=True))
    def get(self):
        try:
            res = Course.query.filter(and_(Course.status == "published", Course.visibility == "public")).all()
            if res == None:
                raise Exception("The Course id is not listed", HTTPStatus.NOT_FOUND)

            return res
        
        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
            logging.exception(error_message)
            error_message = {
                'error': error_message,
                'status': status_code
            }
            error_message = json.dumps(error_message)
            abort(Response(error_message, status_code, mimetype='application/json'))

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
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
            logging.exception(error_message)
            error_message = {
                'error': error_message,
                'status': status_code
            }
            error_message = json.dumps(error_message)
            abort(Response(error_message, status_code, mimetype='application/json'))

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
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
            logging.exception(error_message)
            error_message = {
                'error': error_message,
                'status': status_code
            }
            error_message = json.dumps(error_message)
            abort(Response(error_message, status_code, mimetype='application/json'))

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
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
            logging.exception(error_message)
            error_message = {
                'error': error_message,
                'status': status_code
            }
            error_message = json.dumps(error_message)
            abort(Response(error_message, status_code, mimetype='application/json'))
 
    def delete(self, id):
        try:
            res = Course.query.filter(and_(Course.id == id, Course.status == "published")).first()

            if res == None:
                raise Exception("The Course id is not listed", HTTPStatus.NOT_FOUND)

            res.status = "Deleted"
            db.session.commit()

            return {'message':'Course successfully Deleted',"status": HTTPStatus.OK}
        
        except Exception as e:
            error_message = str(e.args[0]) if e.args else 'An error occurred'
            status_code = e.args[1] if len(e.args) > 1 else HTTPStatus.INTERNAL_SERVER_ERROR
            logging.exception(error_message)
            error_message = {
                'error': error_message,
                'status': status_code
            }
            error_message = json.dumps(error_message)
            abort(Response(error_message, status_code, mimetype='application/json'))

@api.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return {e.messages, HTTPStatus.BAD_REQUEST}