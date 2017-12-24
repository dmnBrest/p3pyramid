from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from pyramid.view import forbidden_view_config, view_config

from ..models import User

import logging
log = logging.getLogger(__name__)

@view_config(route_name='auth_login', renderer='../templates/auth/login.jinja2')
def login(request):
    next_url = request.params.get('next', request.referrer)
    if not next_url:
        next_url = request.route_url('home')
    message = ''
    login = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        user = request.dbsession.query(User).filter_by(username=login).first()
        if user is not None and user.check_password(password):
            headers = remember(request, user.id)
            return HTTPFound(location=next_url, headers=headers)
        message = 'Failed login'

    return dict(
        message=message,
        url=request.route_url('auth_login'),
        next_url=next_url,
        login=login,
    )

@view_config(route_name='auth_logout')
def logout(request):
    headers = forget(request)
    next_url = request.route_url('home')
    return HTTPFound(location=next_url, headers=headers)

@forbidden_view_config()
def forbidden_view(request):
    next_url = request.route_url('auth_login', _query={'next': request.url})
    return HTTPFound(location=next_url)


# @view_config(route_name='auth_register', request_method='GET', renderer='../templates/auth/register.jinja2')
# def register(request):
#
#     return {}