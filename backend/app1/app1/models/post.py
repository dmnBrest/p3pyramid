import datetime as dt

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
    DateTime
)
from sqlalchemy.orm import relationship

from marshmallow import fields

from .meta import Base

from ..helpers import RenderSchema

class PostRenderSchema(RenderSchema):
    created_at = fields.DateTime()
    class Meta:
        additional = ('id', 'title', 'slug', 'content', 'user_id', 'user', 'comments')

class Post(Base):
    __tablename__ = 'posts'
    __render_schema__ = PostRenderSchema()
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    slug = Column(Text, nullable=False, unique=True)
    content = Column(Text, nullable=False)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref='posts')
    created_at = Column(DateTime, default=dt.datetime.utcnow, nullable=False)