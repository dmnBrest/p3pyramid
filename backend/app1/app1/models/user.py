import bcrypt
import datetime as dt
from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime
)
from marshmallow import fields

from .meta import Base

from ..helpers import RenderSchema

class UserRenderSchema(RenderSchema):
    created_at = fields.DateTime()
    class Meta:
        additional = ('id', 'username', 'email', 'role')

class User(Base):
    """ The SQLAlchemy declarative model class for a User object. """
    __tablename__ = 'users'
    __render_schema__ = UserRenderSchema()
    id = Column(Integer, primary_key=True)
    username = Column(Text, nullable=False, unique=True)
    email = Column(Text, nullable=False, unique=True)
    role = Column(Text, nullable=False)
    password_hash = Column(Text)
    created_at = Column(DateTime, default=dt.datetime.utcnow, nullable=False)

    def set_password(self, pw):
        pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
        self.password_hash = pwhash.decode('utf8')

    def check_password(self, pw):
        if self.password_hash is not None:
            expected_hash = self.password_hash.encode('utf8')
            return bcrypt.checkpw(pw.encode('utf8'), expected_hash)
        return False