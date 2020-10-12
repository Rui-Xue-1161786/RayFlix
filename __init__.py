from flask import Flask
import os
from datafilereaders import repository as repo
from datafilereaders.memory_repository import MemoryRepository


def create_app():
    app = Flask(__name__)

    # # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    # data_path = os.path.join('covid', 'adapters', 'data')

    file_path = '/Users/rayxue/Downloads/RayFlix-master/datafiles/Data1000Movies.csv'
    repo.repo_instance = MemoryRepository(file_path)
    with app.app_context():
        # Register blueprints.
        from home import home
        app.register_blueprint(home.home_blueprint)

        from family import family
        app.register_blueprint(family.family_blueprint)

        from authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from watching import watching
        app.register_blueprint(watching.watching_blueprint)

        # from .utilities import utilities
        # app.register_blueprint(utilities.utilities_blueprint)

    return app
