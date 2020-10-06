import pytest

from domainmodel.model import Movie, Genre, User, Review,Actor, WatchList, Director


@pytest.fixture()
def movie():
    return Movie('The story of Ray', 2020)


@pytest.fixture()
def director():
    return Director('Ray Xue')


@pytest.fixture()
def genre():
    return Genre('Documentary')


@pytest.fixture()
def review(movie):
    return Review(movie, 'Interesting!', 10)


@pytest.fixture()
def user():
    return User('ray123','123')


@pytest.fixture()
def watchlist():
    return WatchList()


def test_movie_construction(movie):
    assert movie.title == 'The story of Ray'
    assert movie.release_year == 2020
    assert movie.__repr__() == '<Movie The story of Ray, 2020>'


def test_directer_construction(director):
    assert director.director_full_name == 'Ray Xue'


def test_review_construction(review):
    assert review.movie.__repr__() == '<Movie The story of Ray, 2020>'
    assert review.review_text == 'Interesting!'
    assert review.rating == 10


def test_watchlist_construction(watchlist, movie):
    assert watchlist.size() == 0
    watchlist.add_movie(movie)
    assert  watchlist.size() == 1
    assert watchlist.watch_list == [movie]
    watchlist.remove_movie(movie)
    assert watchlist.size() == 0

