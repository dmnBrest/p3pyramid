from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship

from .meta import Base

from ..helpers import RenderSchema

class CommentRenderSchema(RenderSchema):

    class Meta:
        additional = ('id', 'content', 'user_id', 'post_id')

class Comment(Base):
    """ The SQLAlchemy declarative model class for a Page object. """
    __tablename__ = 'comments'
    __render_schema__ = CommentRenderSchema()
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref='comments')
    post_id = Column(ForeignKey('posts.id'), nullable=False)
    post = relationship('Post', backref='comments')