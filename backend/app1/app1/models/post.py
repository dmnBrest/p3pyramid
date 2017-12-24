from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship

from .meta import Base

from ..helpers import RenderSchema

class PostRenderSchema(RenderSchema):

    class Meta:
        additional = ('id', 'title', 'slug', 'content', 'user_id')

class Post(Base):
    __tablename__ = 'posts'
    __render_schema__ = PostRenderSchema()
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    slug = Column(Text, nullable=False, unique=True)
    content = Column(Text, nullable=False)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref='posts')