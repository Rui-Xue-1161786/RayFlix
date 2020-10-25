from flask import Flask
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

from datafilereaders import repository as repo
from datafilereaders import memory_repository, database_repository
from datafilereaders.orm import metadata, map_model_to_tables


def create_app():
    app = Flask(__name__)

    # # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    file_path = 'datafiles/Data1000Movies.csv'

    if app.config['REPOSITORY'] == 'memory':
        repo.repo_instance = memory_repository.MemoryRepository(file_path)

    elif app.config['REPOSITORY'] == 'database':
        # Configure database.

        database_uri = app.config['SQLALCHEMY_DATABASE_URI']

        # We create a comparatively simple SQLite database, which is based on a single file (see .env for URI).
        database_echo = app.config['SQLALCHEMY_ECHO']
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=database_echo)

        if len(database_engine.table_names()) == 0:
            metadata.create_all(database_engine)  # Conditionally create database tables.
            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()
            database_repository.populate(database_engine, file_path)

        else:
            # Solely generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

        # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
        repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)


    with app.app_context():
        # Register blueprints.
        from home import home
        app.register_blueprint(home.home_blueprint)

        # from search import search
        # app.register_blueprint(search.family_blueprint)

        from authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from watching import watching
        app.register_blueprint(watching.watching_blueprint)

        from utilities import utilities
        app.register_blueprint(utilities.utilities_blueprint)

    return app
