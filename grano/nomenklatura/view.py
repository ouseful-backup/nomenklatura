import os
from json import dumps

from flask import Blueprint, render_template
from flask import make_response

from grano import __version__
from grano.core import app, url_for, app_name


UI_PREFIX = app.config.get('NOMENKLATURA_PREFIX', '')
STATIC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                              '../../static'))

blueprint = Blueprint('nomenklatura', __name__, template_folder=STATIC_PATH,
                      static_folder=STATIC_PATH)


def angular_templates():
    partials_dir = os.path.join(STATIC_PATH, 'templates')
    for (root, dirs, files) in os.walk(partials_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, 'rb') as fh:
                file_name = file_path[len(partials_dir) + 1:]
                yield (file_name, fh.read().decode('utf-8'))


@blueprint.route('/')
def index(**kw):
    return render_template('layout.html',
                           angular_templates=angular_templates())


@blueprint.route('/config.js')
def config(**kw):
    api_root = app.config.get('API_ROOT') or url_for('base_api.status')
    res = render_template('js/config.js',
                          ui_root=url_for('nomenklatura.index'),
                          schema_objs=dumps(app.config['SCHEMA_OBJS']),
                          api_root=api_root,
                          app_name=app_name,
                          app_version=__version__)
    res = make_response(res)
    res.headers['Content-Type'] = 'application/javascript'
    return res
