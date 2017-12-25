def includeme(config):
    config.add_route('auth_login', '/auth/login')
    config.add_route('auth_logout', '/auth/logout')
    config.add_route('auth_register', '/auth/register')
    config.add_route('blog_index', '/blog')
    config.add_route('get_posts', '/api/v0/post')
    config.add_route('get_post', '/api/v0/post/{slug}')
    #config.add_route('save_post', 'api/v0/post/{post_id}')
    config.add_route('home', '/')
    config.add_static_view('static', 'static', cache_max_age=3600)
