__author__ = "Vitali Muladze"

from typing import Any

from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()


def create_app(config: Any) -> Flask:
    app = Flask(__name__,
                static_folder="../statics",
                template_folder="../templates")

    app.config.from_object(config)
    config.init_app(app)

    mongo.init_app(app)
    # Register blueprints
    from .analytics import analytics_app

    app.register_blueprint(analytics_app)
    return app
