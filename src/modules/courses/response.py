from flask_marshmallow import Marshmallow
from marshmallow.fields import String, Integer, List, Nested
from marshmallow import validate, Schema

ma = Marshmallow()

class ChapterSchema(Schema):
    id = Integer(required=True, dump_only=True)
    title = String(required=True, dump_only=True)
    content = String(required=True, dump_only=True)
    description = String(required=True, dump_only=True)
    videoLink = String(required=True, dump_only=True)
    duration = Integer(required=True, dump_only=True)

class CourseResponse(ma.SQLAlchemyAutoSchema):
    id = Integer(required=True, dump_only=True)
    title = String(required=True, dump_only=True)
    category = String(required=True, dump_only=True)
    description = String(required=True, dump_only=True)
    duration = Integer(required=True, dump_only=True)
    instructor_name = String(required=True, dump_only=True)
    language = String(required=True, dump_only=True)
    level = String(required=True, dump_only=True)
    price = Integer(required=True, dump_only=True)
    status = String(required=True, dump_only=True)
    visibility = String(required=True, dump_only=True)
    chapters = List(Nested(ChapterSchema), required=True, dump_only=True)