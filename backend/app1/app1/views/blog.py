from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound,
    HTTPNotFound,
)

from ..models import Post

import logging
log = logging.getLogger(__name__)

@view_config(route_name='blog_index', renderer='../templates/blog/index.jinja2')
def blog_index(request):
    return {
        'initial_data': {
            'someVar': 'XXXXX'
        }
    }

@view_config(route_name='get_posts', renderer='json')
def get_posts(request):

    posts = request.dbsession.query(Post).all()

    return {
        'posts': posts
    }

@view_config(route_name='get_post', renderer='json')
def get_post(request):

    return {
        'post': {'id': '11111', 'title': 'Post #1'}
    }