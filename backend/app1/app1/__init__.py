import os
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.csrf import SessionCSRFStoragePolicy

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings = expandvars_dict(settings)
    config = Configurator(settings=settings)

    config.set_csrf_storage_policy(SessionCSRFStoragePolicy)
    #config.set_default_csrf_options(require_csrf=True)

    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.include('.security')

    my_session_factory = SignedCookieSessionFactory('00000000100010001000001')
    config.set_session_factory(my_session_factory)

    config.scan()
    return config.make_wsgi_app()

def expandvars_dict(settings):
    """Expands all environment variables in a settings dictionary."""
    return dict((key, os.path.expandvars(value)) for
                key, value in settings.items())
