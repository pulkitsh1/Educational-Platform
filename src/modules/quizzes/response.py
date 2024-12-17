from flask_marshmallow import Marshmallow
from marshmallow.fields import String, Integer, List, Nested
from marshmallow import validate, Schema

ma = Marshmallow()

class QuestionSchema(Schema):
    id = Integer(required=True, dump_only=True)
    question = String(required=True, dump_only=True)
    options = String(required=True, dump_only=True)
    answer = String(required=True, dump_only=True)
    quizz_id = Integer(required=True, dump_only=True)

class QuizzResponse(ma.SQLAlchemyAutoSchema):
    id = Integer(required=True, dump_only=True)
    course_id = Integer(required=True, dump_only=True)
    status = String(required=True, dump_only=True)
    questions = List(Nested(QuestionSchema), required=True, dump_only=True)