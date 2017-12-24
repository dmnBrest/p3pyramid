from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData

# Recommended naming convention used by Alembic, as various different database
# providers will autogenerate vastly different names making migrations more
# difficult. See: http://alembic.zzzcomputing.com/en/latest/naming.html
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

class Base(object):
    """
    Provides JSON-serialization for our SQLAlchemy-objects.

    Every SQLAlchemy model nees to set a marshmallow-schema as class-attribute
    ``__render_schema__``, for example:

    __render_schema__ = SomeSchema()

    This schema will then be used for serialization of instances of that class.
    Additionally, the ``request`` object can be extend with a dictionary that maps
    classes to schemas, e.g.:

    request.render_schemas = {Package: PackageRenderSchema(exclude=('availabilities',))}

    See also:
    http://docs.sqlalchemy.org/en/rel_1_0/orm/extensions/declarative/mixins.html#augmenting-the-base
    """
    def __json__(self, request):
        render_schemas = getattr(request, 'render_schemas', {})
        # Fall back on self.__render_schema__ when there was no schema defined for this class in this request.
        schema = render_schemas.get(self.__class__) or self.__render_schema__
        # TODO: Add error handling
        result, errors = schema.dump(self)
        return result


metadata = MetaData(naming_convention=NAMING_CONVENTION)
Base = declarative_base(cls=Base, metadata=metadata)
