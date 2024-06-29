"""
A Python3 tool for evaluating design systems.
"""


from flask import Flask


__version__ = '0.1.0'


def create_app(injected_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')

    if injected_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(injected_config)

    # Application views, configuration will be defined here.
    @app.route('/')
    def index():
        return 'Greetings, programs!'

    return app
