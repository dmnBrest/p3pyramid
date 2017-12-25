from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.orm import joinedload

from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound,
    HTTPNotFound,
)

from ..models import Post, User
from ..models.user import UserRenderSchema
from ..models.post import PostRenderSchema

import logging
log = logging.getLogger(__name__)

@view_config(route_name='blog_index', renderer='../templates/blog/blog.jinja2')
def blog_index(request):
    return {
        'initial_data': {
            'someVar': 'XXXXX'
        }
    }

@view_config(route_name='get_posts', renderer='json')
def get_posts(request):

    posts = request.dbsession.query(Post).all()

    request.render_schemas = {
        Post: PostRenderSchema(exclude=('content',)),
        User: UserRenderSchema(only=('id', 'username',))
    }

    return {
        'posts': posts
    }

@view_config(route_name='get_post', renderer='json')
def get_post(request):

    print(request.matchdict)

    slug = request.matchdict['slug']

    post = request.dbsession.query(Post).options(joinedload('comments')).filter_by(slug=slug).first()

    request.render_schemas = {
        User: UserRenderSchema(only=('id', 'username',))
    }

    return {
        'post': post
    }