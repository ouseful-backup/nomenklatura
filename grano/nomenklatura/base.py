from flask import url_for

from flask.ext.assets import Environment
#from flask.ext.assets import ManageAssets

from grano.core import app
from grano.interface import Startup
from grano.nomenklatura.view import blueprint, STATIC_PATH, UI_PREFIX


assets = Environment(app)


@app.before_request
def configure_assets():
    if len(UI_PREFIX):
        assets.url = url_for('nomenklatura.static', filename='')
    

class Installer(Startup):

    def configure(self, manager):
        if len(UI_PREFIX):
            assets.directory = STATIC_PATH
            assets.url = UI_PREFIX + '/static'
        #manager.add_command("assets", ManageAssets(assets))
        app.register_blueprint(blueprint, url_prefix=UI_PREFIX)
        

