from flask_marshmallow import Marshmallow
from marshmallow.fields import String, Integer, List, Nested
from marshmallow import validate, validates_schema, ValidationError, Schema

ma = Marshmallow()

class ChapterSchema(Schema):
    title = String(required=True,validate=[validate.Length(min=3)], load_only=True)
    content = String(required=True, load_only=True)
    description = String(required=True, load_only=True)
    videoLink = String(required=True, load_only=True)
    duration = Integer(required=True, load_only=True)

class Post_req(ma.SQLAlchemyAutoSchema):
    title = String(required=True,validate=[validate.Length(min=3)], load_only=True)
    category = String(required=True, load_only=True)
    description = String(required=True, load_only=True)
    duration = Integer(required=True, load_only=True)
    instructor_name = String(required=True, load_only=True)
    language = String(required=True, load_only=True)
    level = String(required=True, load_only=True)
    price = Integer(required=True, load_only=True)
    status = String(required=True, load_only=True)
    visibility = String(required=True, load_only=True)
    chapters = List(Nested(ChapterSchema), required=True, validate=validate.Length(min=1))


class Put_req(ma.SQLAlchemyAutoSchema):
    chapters = List(Nested(ChapterSchema), required=True, validate=validate.Length(min=1))

    @validates_schema
    def validate_chapters(self, data, **kwargs):
        if not isinstance(data.get("chapters"), list):
            raise ValidationError("Chapters must be a list of JSON objects.", field_name="chapters")
        for chapter in data["chapters"]:
            if not isinstance(chapter, dict):
                raise ValidationError("Each chapter must be a JSON object.", field_name="chapters")