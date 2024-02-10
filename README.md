# Flasket

Micro blog powered by Flask and flat files that can be compiled to a static site.

## Quickstart

1. Install dependencies

    `python -m venv venv`

    `source venv/bin/activate`

    `pip install -r requirements.txt`

2. Run the development server for local testing

    `flask run`

    or `FLASK_ENV=development flask run` if you need need auto-reloading on python/template changes (not needed for editing posts)

3. Build a production ready static version of the site

    `flask freeze`

4. To test out the built static site you can use the http.server module

    `cd ./build && python -m http.server 8000`

    Then open the browser to [localhost:8000](http://localhost:8000/)
    
## Demo Site

[https://carc1n0gen.github.io/flasket/](https://carc1n0gen.github.io/flasket/)

## Writing Blog Posts

Just create markdown files with a name like `YYYY-MM-DD-post-title.md` in the posts folder and they will be instantly visible when running the development server, and in the built static site the next time you run the freeze command. Posts don't support jinja template syntax.

A file named `2020-10-25-hello-world.md` will be accessible at `http://example.com/2020/10/25/hello-world/`

## Creating Regular Pages

Create html files (which are actually jinja template files) in the templates/pages folder and they will be instantly visible

A file named `about.html` will be accessible at `http://example.com/about/`

A file in the folder `foo` and called `bar.html` will be accessible at `http://example.com/foo/bar/`

When creating these pages, you can extend/include template from the configured theme with `theme('template_name.html')`, otherwise if you want to refer to your own templates from the templates folder use just plain `'template_name.html'`.

example:

```jinja
{# extend or include a theme template file #}
{% extends theme('base.html') %}
{% include theme('nav.html') %}

{# extend or include one of your own template files #}
{% extends 'base.html' %}
{% include 'nav.html' %}
```

## Themes

Themes go in the themes folder (imagine that!).  At a minimum, a theme must have the following 5 templates: `404.html`, `blog.html`, `feed.xml`, `page.html`, `post.html`.  A theme can have as many additional templates/includes as it wishes, these are just the main ones required.  Additionally, a theme needs a `static` folder along side those template files, if the theme should ship with static files like css/js/images.

You can override the themes version of these 5 templates by putting a template with the same file name in the templates folder. This is the favoured approach over editing the theme directly.  Of course if you find yourself wanting to override _everything_, you could copy the whole theme to a new one also.

A theme may provide pages in the pages folder within the theme.  These pages can also be overridden by just creating your own page with the same name.

# Deploying to Github Pages

Here is an example github actions configuration file that will deploy the static site to Github Pages.  Paste it in a new file `/.github/workflows/main.yml` in your repo.

```yml
name: Build and deploy to github pages
on:
  push:
    branches: [ main ] # Change this to the branch you want to have build every push

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up python 3.8
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      
      - name: Install dependencies and build
        run: |
          pip install -r requirements.txt
          flask freeze

      - name: Deploy
        uses: JamesIves/github-pages-deploy-action@3.7.1
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          BRANCH: gh-pages
          FOLDER: build
          CLEAN: true
```

Additionally, if you want to deploy to Github Pages on a repo other than `<username>.github.io` (which makes them sort of like a subdirectory on your main Github Pages site), you will want to add an additional configuration to config.yml in order for generated urls to be correct.

`FREEZER_BASE_URL: http://<username>.github.io/<repo-name>/`
