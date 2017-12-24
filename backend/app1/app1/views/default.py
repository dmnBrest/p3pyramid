from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound,
    HTTPNotFound,
)

import logging
log = logging.getLogger(__name__)

@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
def my_view(request):
    try:

        # query = request.dbsession.query(MyModel)
        # one = query.filter(MyModel.name == 'one').first()

        user = request.user
        log.debug('current user:')
        log.debug(user)
        # if user is None or (user.role != 'editor' and page.creator != user):
        #     raise HTTPForbidden
        # if user is None or user.role not in ('editor', 'basic'):
        #     raise HTTPForbidden

        request.session.flash('mymessageX')

        if 'counter' in request.session:
            request.session['counter'] += 1
        else:
            request.session['counter'] = 0

        log.debug(request.session['counter'])

        log.debug(request.session.peek_flash())

    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)

    return {}


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_app1_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
