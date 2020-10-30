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


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)
    u = None
    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('Dave')

    assert user2 == u

def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    u = None
    user = repo.get_user('fmercury')
    assert user == u

def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    u = None
    user = repo.get_user('prince')
    assert user is u


