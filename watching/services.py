from typing import List, Iterable

from datafilereaders.repository import AbstractRepository
from domainmodel.model import User, Genre


class NonExistentArticleException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def get_movie_ids_by_tags(tag_name: str, repo: AbstractRepository):
    id_list = repo.get_movie_ids_for_genre(tag_name)

    if id_list is None:
        raise NonExistentArticleException

    return id_list


def get_single_page_of_movies(id_list, repo: AbstractRepository):
    movies = repo.get_movie_list_by_id_list(id_list)
    return movies
