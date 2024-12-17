from flask_marshmallow import Marshmallow
from marshmallow.fields import String, Integer, List, Nested
from marshmallow import validate, Schema

ma = Marshmallow()

class QuestionSchema(Schema):
    question = String(required=True, load_only=True)
    options = List(String(), required=True, load_only=True)
    answer = String(required=True, load_only=True)

class Post_req(ma.SQLAlchemyAutoSchema):
    questions = List(Nested(QuestionSchema), required=True, validate=validate.Length(min=1))

class AnswerSchema(Schema):
    question_id = Integer(required=True, load_only=True)
    answer = String(required=True, load_only=True)

class Res_req(ma.SQLAlchemyAutoSchema):
    answers = List(Nested(AnswerSchema), required=True, validate=validate.Length(min=1))
