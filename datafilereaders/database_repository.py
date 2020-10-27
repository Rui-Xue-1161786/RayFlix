import csv
import os

from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.engine import Engine
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from werkzeug.security import generate_password_hash

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from domainmodel.model import User, Movie, Genre, Director, Review, Actor
from datafilereaders.repository import AbstractRepository

tags = None
actors = None


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username) -> User:
        user = None
        try:

            user = self._session_cm.session.query(User).filter_by(_User__username=username).one()
            print("user!!!!!!!!")
            print(user)
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def add_actor(self, actor: Actor):
        pass

    def get_actor(self, actor: Actor) -> Actor:
        pass

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.add(genre)
            scm.commit()

    def get_genre(self) -> List[Genre]:
        genres = self._session_cm.session.query(Genre).all()
        tag_names = []
        for genre in genres:
            tag_names.append(genre.genre_name)
        return tag_names

    def add_review(self, review: Review):
        super().add_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_review(self):
        reviews = self._session_cm.session.query(Review).all()
        return reviews

    def add_director(self, director: Director):
        pass

    def get_director(self, director: str) -> Director:
        pass

    def add_movie(self, movie: Movie):
        with self._session_cm as scm:
            scm.session.add(movie)
            scm.commit()

    def get_movie(self, movie: str) -> Movie:
        movie = None
        try:
            movie = self._session_cm.session.query(Movie).filter_by(_Movie__title=movie).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return movie

    def get_number_of_movies(self):
        print('get number of movies count')
        number_of_movies = self._session_cm.session.query(Movie).count()
        return number_of_movies

    def get_all_movie(self):
        print('get all movies')
        movies = self._session_cm.session.query(Movie).all()
        return movies

    def get_movie_by_id(self, id: int):
        print(' get movie by id')
        movie = self._session_cm.session.query(Movie).filter_by(_Movie__id=id).one()
        return movie

    def get_movie_ids_for_genre(self, genre_name: str):
        movie_ids = []

        # Use native SQL to retrieve article ids, since there is no mapped class for the article_tags table.
        row = self._session_cm.session.execute('SELECT id FROM tags WHERE genre_name = :tag_name',
                                               {'tag_name': genre_name}).fetchone()

        if row is None:
            # No tag with the name tag_name - create an empty list.
            movie_ids = list()
        else:
            tag_id = row[0]

            # Retrieve article ids of articles associated with the tag.
            movie_ids = self._session_cm.session.execute(
                'SELECT movie_id FROM movie_tags WHERE tag_id = :tag_id ORDER BY movie_id ASC',
                {'tag_id': tag_id}
            ).fetchall()
            movie_ids = [id[0] for id in movie_ids]

        return movie_ids

    def get_movie_list_by_id_list(self, id_list):
        name_list = []
        # user = self._session_cm.session.query(User).filter_by(_User__username=username).one()
        for id in id_list:
            movie = self._session_cm.session.query(Movie).filter_by(_Movie__id=id).one()
            name_list.append(movie)
        return name_list

    def get_movie_by_name(self, title: str):
        movie_list = []
        try:
            movies = self._session_cm.session.query(Movie).filter_by(_Movie__title=title).all()
            for movie in movies:
                movie_list.append(movie)
        except:
            pass
        try:
            movies = self._session_cm.session.query(Movie).filter_by(_Movie__director_full_name=title).all()
            for movie in movies:
                movie_list.append(movie)
        except:
            pass

        try:
            row = self._session_cm.session.execute('SELECT id FROM Actors WHERE actor_full_name = :actor_name',
                                                   {'actor_name': title}).fetchone()
            if row is None:
                # No tag with the name tag_name - create an empty list.
                movie_ids = list()
            else:
                actor_id = row[0]

                # Retrieve article ids of articles associated with the tag.
                movie_ids = self._session_cm.session.execute(
                    'SELECT movie_id FROM movie_actors WHERE actor_id = :actor_id ORDER BY movie_id ASC',
                    {'actor_id': actor_id}
                ).fetchall()
                movie_ids = [id[0] for id in movie_ids]
                for movie_id in movie_ids:
                    movies = self._session_cm.session.query(Movie).filter_by(_Movie__id=movie_id).all()
                    for movie in movies:
                        movie_list.append(movie)
        except:
            pass

        return movie_list

    def get_director_list(self):
        pass

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()


def movie_record_generator(filename: str):
    with open(filename, mode='r', encoding='utf-8-sig') as infile:
        reader = csv.DictReader(infile)

        # # Read first line of the CSV file.
        # headers = next(reader)
        # Read remaining rows from the CSV file.
        for row in reader:
            movie_data = list()
            movie_id = int(row['Rank'])
            movie_data.append(movie_id)
            movie_data.append(int(row['Year']))
            movie_data.append(row['Title'])
            movie_data.append(row['Description'])
            movie_data.append(row['Director'])

            movie_tags = row['Genre'].split(',')
            for tag in movie_tags:
                if tag not in tags.keys():
                    tags[tag] = list()
                tags[tag].append(movie_id)

            movie_actors = row['Actors'].split(',')
            for actor in movie_actors:
                actor = actor.strip()
                if actor not in actors.keys():
                    actors[actor] = list()
                actors[actor].append(movie_id)

            yield movie_data


def get_tag_records():
    tag_records = list()
    tag_key = 0

    for tag in tags.keys():
        tag_key = tag_key + 1
        tag_records.append((tag_key, tag))
    return tag_records


def get_actor_records():
    actor_records = list()
    actor_key = 0

    for actor in actors.keys():
        actor_key = actor_key + 1
        actor_records.append((actor_key, actor))
    return actor_records


def movie_tags_generator():
    movie_tags_key = 0
    tag_key = 0

    for tag in tags.keys():
        tag_key = tag_key + 1
        for movie_key in tags[tag]:
            movie_tags_key = movie_tags_key + 1
            yield movie_tags_key, movie_key, tag_key


def movie_actors_generator():
    movie_actors_key = 0
    actor_key = 0

    for actor in actors.keys():
        actor_key = actor_key + 1
        for movie_key in actors[actor]:
            movie_actors_key = movie_actors_key + 1
            yield movie_actors_key, movie_key, actor_key


# def generic_generator(filename, post_process=None):
#     with open(filename) as infile:
#         reader = csv.reader(infile)
#
#         # Read first line of the CSV file.
#         next(reader)
#
#         # Read remaining rows from the CSV file.
#         for row in reader:
#             # Strip any leading/trailing white space from data read.
#             row = [item.strip() for item in row]
#
#             if post_process is not None:
#                 row = post_process(row)
#             yield row


# def process_user(user_row):
#     user_row[2] = generate_password_hash(user_row[2])
#     return user_row


def populate(engine: Engine, data_path: str):
    conn = engine.raw_connection()
    cursor = conn.cursor()

    global tags
    tags = dict()

    global actors
    actors = dict()

    insert_movies = """
        INSERT INTO movies (
        id, release_year, title, description, director_full_name)
        VALUES (?, ?, ?, ?, ?)"""
    cursor.executemany(insert_movies, movie_record_generator(data_path))

    insert_tags = """
        INSERT INTO tags (
        id, genre_name)
        VALUES (?, ?)"""
    cursor.executemany(insert_tags, get_tag_records())

    insert_actors = """
            INSERT INTO actors (
            id, actor_full_name)
            VALUES (?, ?)"""
    cursor.executemany(insert_actors, get_actor_records())

    insert_movie_tags = """
        INSERT INTO movie_tags (
        id, movie_id, tag_id)
        VALUES (?, ?, ?)"""
    cursor.executemany(insert_movie_tags, movie_tags_generator())

    insert_movie_actors = """
            INSERT INTO movie_actors (
            id, movie_id, actor_id)
            VALUES (?, ?, ?)"""
    cursor.executemany(insert_movie_actors, movie_actors_generator())

    # insert_users = """
    #     INSERT INTO users (
    #     id, username, password)
    #     VALUES (?, ?, ?)"""
    # cursor.executemany(insert_users, generic_generator(os.path.join(data_path, 'users.csv'), process_user))

    # insert_comments = """
    #     INSERT INTO comments (
    #     id, user_id, article_id, comment, timestamp)
    #     VALUES (?, ?, ?, ?, ?)"""
    # cursor.executemany(insert_comments, generic_generator(os.path.join(data_path, 'comments.csv')))

    conn.commit()
    conn.close()
