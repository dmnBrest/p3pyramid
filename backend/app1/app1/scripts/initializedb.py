import os
import sys
import uuid
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )

from ..models import User
from ..models import Post
from ..models import Comment

from app1 import expandvars_dict

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    settings = expandvars_dict(settings)

    engine = get_engine(settings)

    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        editor = User(username='doom1', email='doom1@doom1.com', role='editor')
        editor.set_password('doom1')
        dbsession.add(editor)

        basic = User(username='doom2', email='doom2@doom2.com', role='basic')
        basic.set_password('doom2')
        dbsession.add(basic)

        post1 = Post(
            title='Post #1',
            slug=uuid.uuid4(),
            user=editor,
            content='This is the front page',
        )
        dbsession.add(post1)

        comment1 = Comment(
            user=basic,
            post=post1,
            content='This comment for Post #1'
        )
        dbsession.add(comment1)
        comment2 = Comment(
            user=editor,
            post=post1,
            content='This comment 2 for Post #1',
        )
        dbsession.add(comment2)

        post2 = Post(
            title='Post #2',
            slug=uuid.uuid4(),
            user=editor,
            content='Post #2 Content',
        )
        dbsession.add(post2)
        comment3 = Comment(
            user=basic,
            post=post2,
            content='This comment for Post #2'
        )
        dbsession.add(comment3)
        comment4 = Comment(
            user=editor,
            post=post2,
            content='This comment 2 for Post #2',
        )
        dbsession.add(comment4)
