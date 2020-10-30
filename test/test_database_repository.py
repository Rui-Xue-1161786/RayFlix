import pytest
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from datafilereaders import memory_repository, database_repository
from datafilereaders.database_repository import SqlAlchemyRepository
from domainmodel.model import User
from datafilereaders.orm import metadata, map_model_to_tables
from datafilereaders.repository import RepositoryException
from flask import Flask
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

from datafilereaders import repository as repo
from datafilereaders import memory_repository, database_repository
from datafilereaders.orm import metadata, map_model_to_tables


def test_repository_can_add_a_user():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    file_path = '/Users/rayxue/Downloads/RayFlix-master/datafiles/Data1000Movies.csv'
    if app.config['REPOSITORY'] == 'database':
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        database_echo = app.config['SQLALCHEMY_ECHO']
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=database_echo)
        if len(database_engine.table_names()) == 0:
            metadata.create_all(database_engine)  # Conditionally create database tables.
            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()
            database_repository.populate(database_engine, file_path)
        else:
            map_model_to_tables()
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    user = User('Dave', '123456789')
    assert user == User('Dave', '123456789')
    repo.repo_instance.add_user(user)
    repo.repo_instance.add_user(User('Martin', '123456789'))
    user2 = repo.repo_instance.get_user('Dave')
    print('??')
    print(user2)
    # assert user2 == user and user2 is user

test_repository_can_add_a_user()
