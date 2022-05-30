import os
import yaml
from datetime import datetime
from flask import Flask, render_template
from flask_frozen import Freezer
from flask_themer import Themer, render_template as render_theme_template
from .posts import get_post, get_posts
from .paginator import paginator
from .globals import init_globals


app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.update({
   'BASE_URL': '',
   'THEMER_DEFAULT_DIRECTORY': '../themes',
   'FREEZER_DESTINATION': '../build',
   'FREEZER_STATIC_IGNORE': ['.gitkeep']
})
app.config.from_file('../config.yml', yaml.safe_load)


freezer = Freezer(app)
themer = Themer(app)
init_globals(app)


@themer.current_theme_loader
def get_current_theme():
    return app.config.get('THEME', 'minima') 


@app.cli.command()
def freeze():
   """Generate a static site from the flask app"""
   freezer.freeze()


@app.route('/404.html')
def notfound():
   try:
      return render_template('404.html')
   except:
      return render_theme_template('404.html')


@app.route('/')
@app.route('/<int:page>/')
def blog(page=1):
   paginator.page = page
   try:
      return render_template('blog.html', paginator=paginator)
   except:
      return render_theme_template('blog.html', paginator=paginator)


@freezer.register_generator
def blog():
   for n in range(1, paginator.total_pages):
      yield { 'page': n + 1 }


@app.route('/<path:path>/')
def page(path):
   try:
      return render_template(f'pages/{path}.html')
   except:
      return render_theme_template(f'pages/{path}.html')


def walk_pages(folder, path_list=[]):
   for filename in os.listdir(folder):
      fpath = os.path.join(folder, filename)
      if os.path.isdir(fpath):
         yield from walk_pages(fpath, (path_list + [filename]))
      else:
         yield f'{"".join(path_list)}/{filename}'


@freezer.register_generator
def page():
   theme_pages = list(walk_pages(f'./themes/{themer.current_theme}/pages'))
   user_pages = list(walk_pages('./templates/pages'))
   for filename in list(set(theme_pages) | set(user_pages)): # Combines two lists without creating duplicates
      if filename.endswith('.html'):
         yield { 'path': filename[:-5] }


@app.route('/<year>/<month>/<day>/<slug>/')
def post(year, month, day, slug):
   post = get_post(f'{year}-{month}-{day}-{slug}.md')
   try:
      return render_template('post.html', posts=posts)
   except:
      return render_theme_template('post.html', post=post)


@freezer.register_generator
def post():
   for post in get_posts():
      yield {
         'year': post['date'].year,
         'month': post['date'].strftime('%m'),
         'day': post['date'].strftime('%d'),
         'slug': post['slug']
      }


@app.route('/feed.xml')
def feed():
   now = datetime.utcnow()
   try:
      return render_template('feed.xml', posts=get_posts(), now=now), { 'Content-type': 'application/xml' }
   except:
      return render_theme_template('feed.xml', posts=get_posts(), now=now), { 'Content-type': 'application/xml' }

