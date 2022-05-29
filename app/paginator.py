import functools
from flask import g, url_for, current_app
from werkzeug.local import LocalProxy
from .posts import get_posts


def context_cached(f):
    """Cache things you only want to calculate once per app/request context."""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        name = f'_cached_{f.__name__}'
        if name not in g:
            setattr(g, name, f(*args, **kwargs))
        return getattr(g, name)
    return wrapper


class Paginator:
    def __init__(self, per_page):
        self.per_page = per_page

        self.page = 1

    @property
    @context_cached
    def _posts(self):
        return get_posts()

    @property
    @context_cached
    def posts(self):
        index = self.page - 1
        return self._posts[index:index + self.per_page]

    @property
    @context_cached
    def total_posts(self):
        return len(self._posts)

    @property
    def total_pages(self):
        if self.total_posts < self.per_page:
            return 1

        return int(self.total_posts / self.per_page)

    @property
    def previous_page(self):
        if self.page == 1:
            return None
        return self.page - 1

    @property
    def previous_page_path(self):
        if self.previous_page == 1:
            return url_for('blog')
        return url_for('blog', page=self.previous_page)

    @property
    def next_page(self):
        if self.page == self.total_pages:
            return None
        return self.page + 1

    @property
    def next_page_path(self):
        return url_for('blog', page=self.next_page)


def get_paginator():
    if 'paginator' not in g:
        g.paginator = Paginator(current_app.config.get('POSTS_PER_PAGE', 5))
    return g.paginator


paginator = LocalProxy(get_paginator)
