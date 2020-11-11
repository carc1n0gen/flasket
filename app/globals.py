from markupsafe import Markup
from werkzeug.local import LocalProxy
from flask import g, current_app, url_for


def get_feed_url():
    return url_for('feed')


feed_url = LocalProxy(get_feed_url)


def get_feed_meta():
    return Markup(
        f'<link type="application/atom+xml" rel="alternate" href="{feed_url}" title="{current_app.config.get("TITLE")}">'
    )


feed_meta = LocalProxy(get_feed_meta)


def init_globals(app):
    app.add_template_global(feed_url, 'feed_url')
    app.add_template_global(feed_meta, 'feed_meta')

    app.add_template_global({
        k.lower(): v for k, v in app.config.items()
    }, 'site')


    app.add_template_filter(lambda page_name, absolute=False: url_for('page', path=page_name, _external=absolute), 'page_url')


