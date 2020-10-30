import pytest

from datafilereaders.memory_repository import MemoryRepository
from domainmodel.model import Movie, Genre, User, Review,Actor, WatchList, Director


@pytest.fixture
def in_memory_repo():
    file_path = '/Users/rayxue/Downloads/RayFlix-master/datafiles/Data1000Movies.csv'
    repo = MemoryRepository(file_path)
    return repo


def test_repository_for_user(in_memory_repo):
    user = User('Dave', '123456789')
    in_memory_repo.add_user(user)
    assert in_memory_repo.get_user('dave') is user
    assert in_memory_repo.get_user('sss') is None
    assert user == User('Dave', '123456789')


def test_repository_for_directer(in_memory_repo):
    assert in_memory_repo.get_director('James Gunn').__repr__() == Director('James Gunn').__repr__()
    director = Director('Ray')
    in_memory_repo.add_director(director)
    assert in_memory_repo.get_director('Ray') == director


def test_repository_for_movie(in_memory_repo):
    movie = Movie('The story of Ray',2020)
    in_memory_repo.add_movie(movie)
    assert in_memory_repo.get_movie('The story of Ray',2020) == movie
    assert in_memory_repo.get_movie('La La Land',2016).__repr__() == Movie('La La Land',2016).__repr__()


def test_repository_for_actor(in_memory_repo):
    assert in_memory_repo.get_actor('Ryan Gosling').__repr__() == Actor('Ryan Gosling').__repr__()
    actor = Actor('Ray')
    in_memory_repo.add_actor(actor)
    assert in_memory_repo.get_actor('Ray') == actor


def test_repository_for_genre(in_memory_repo):
    assert len(in_memory_repo.get_genre()) == 20
    genre = Genre('Good')
    in_memory_repo.add_genre(genre)
    assert len(in_memory_repo.get_genre()) == 21


def test_repository_for_review(in_memory_repo):
    movie = in_memory_repo.get_movie('La La Land', 2016)
    assert len(in_memory_repo.get_review(movie)) == 0
    review = Review(movie,'good',8)
    in_memory_repo.add_review(review)
    assert len(in_memory_repo.get_review(movie)) == 1