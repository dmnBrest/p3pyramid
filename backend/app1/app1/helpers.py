import datetime
import decimal

from marshmallow import Schema, fields
from pyramid.renderers import JSON


def create_json_renderer():
    """
    Return a custom JSON renderer that can handle more types.
    """
    def date_adapter(obj, request):
        return obj.isoformat()

    def decimal_adapter(obj, request):
        return str(obj)

    json_renderer = JSON(indent=4)
    json_renderer.add_adapter(datetime.date, date_adapter)
    json_renderer.add_adapter(decimal.Decimal, decimal_adapter)
    return json_renderer


class RenderSchema(Schema):
    """
    Schema to prevent marshmallow from using its default type mappings.
    """
    TYPE_MAPPING = {}


class CustomFieldsRenderSchema(RenderSchema):
    """
    Schema to add custom_fields in the serialization.
    """
    custom_fields = fields.Dict()
