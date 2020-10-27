from datetime import date, datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from datafilereaders import memory_repository, database_repository
from datafilereaders.database_repository import SqlAlchemyRepository
from domainmodel.model import User
from datafilereaders.orm import metadata, map_model_to_tables
from datafilereaders.repository import RepositoryException


@pytest.fixture
def session_factory():
    TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
    file_path = 'datafiles/Data1000Movies.csv'
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    database_repository.populate(engine, file_path)
    yield session_factory
    metadata.drop_all(engine)
    clear_mappers()



def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('Dave')

    # assert user2 == user and user2 is user
    assert user2 == None