import os
from datetime import datetime
import frontmatter
import misaka as m
from flask import url_for
from pygments import highlight
from pygments.formatters import HtmlFormatter, ClassNotFound
from pygments.lexers import get_lexer_by_name


class HighlighterRenderer(m.HtmlRenderer):
    def blockcode(self, text, lang):
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except ClassNotFound:
            lexer = None

        if lexer:
            formatter = HtmlFormatter()
            return highlight(text, lexer, formatter)
        # default
        return '\n<pre><code>{}</code></pre>\n'.format(text.strip())


renderer = HighlighterRenderer()
md = m.Markdown(renderer, extensions=('fenced-code', 'tables',))


def get_post(file_name):
    post = frontmatter.load(f'./posts/{file_name}')
    date = datetime.strptime(file_name[0:10], '%Y-%m-%d')
    slug = file_name[11:-3]
    title = slug.replace('-', ' ').title()
    html = md(post.content)
    year = date.strftime('%Y')
    month = date.strftime("%m")
    day = date.strftime("%d")
    url = url_for('post', year=year, month=month, day=day, slug=slug)
    feed_url = url_for('post', year=year, month=month, day=day, slug=slug, _external=True)
    return { 
        'title': title,
        'slug': slug,
        'url': url,
        'feed_url': feed_url,
        'content': html,
        'date': date,
        'year': year,
        'month': month,
        'day': day,
        'comments': True,
        **post.metadata
    }


def get_posts():
    files = sorted(os.listdir('./posts'))
    files.reverse()

    return [
        get_post(file)
    for file in files]
