import os

from flask import (Flask, render_template)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says tuki
    @app.route('/tuki')
    def tuki():
        return 'tuki!'
    
    @app.route('/')
    def index():
    
        return render_template('musiquita/index.html')

    from . import auth
    app.register_blueprint(auth.bp) 
    
    from . import db
    db.init_app(app)


    #from . import auth
    #app.register_blueprint(auth.bp)
    
    from . import musiquita
    app.register_blueprint(musiquita.bp)
    app.add_url_rule('/', endpoint='index')

    from . import albums
    app.register_blueprint(albums.bp)
    app.add_url_rule('/', endpoint='index')

    from . import artist
    app.register_blueprint(artist.bp)
    app.add_url_rule('/', endpoint='index')
    
    return app