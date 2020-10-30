from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from domainmodel import model

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    # Column('user_id', ForeignKey('users.id')),
    Column('movie_id', ForeignKey('movies.id')),
    Column('review_text', String(1024), nullable=False),
    Column('timestamp', Date, nullable=True),
    Column('rating', Integer, nullable=True),
    Column('user', String(1024), nullable=False)
)

movies = Table(
    'movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('release_year', Integer, nullable=False),
    Column('title', String(255), nullable=False),
    Column('description', String(1024), nullable=False),
    Column('director_full_name', ForeignKey('directors.director_full_name')),
    Column('rating', Integer, nullable=True),
    Column('rating_count', Integer, nullable=True)
    # Column('hyperlink', String(255), nullable=False),
    # Column('image_hyperlink', String(255), nullable=False)
)

directors = Table(
    'directors', metadata,
    Column('director_full_name', String(255),primary_key=True, nullable=False)
)

actors = Table(
    'actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('actor_full_name', String(255),nullable=False)
)

tags = Table(
    'tags', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('genre_name', String(64), nullable=False)
)

movie_tags = Table(
    'movie_tags', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('tag_id', ForeignKey('tags.id'))
)

movie_actors = Table(
    'movie_actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('actor_id', ForeignKey('actors.id'))
)

user_reviews = Table(
    'user_reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('review_id', ForeignKey('reviews.id'))
)


def map_model_to_tables():
    mapper(model.User, users, properties={
        '_User__username': users.c.username,
        '_User__password': users.c.password
        # MAY NEED TO CHANGE
        # '_reviews': relationship(model.Review, backref='_user')
    })
    mapper(model.Director, directors, properties={
        '_Director__director_full_name': directors.c.director_full_name

    })
    mapper(model.Review, reviews, properties={
        '_Review__movie_id': reviews.c.movie_id,
        '_Review__review_text': reviews.c.review_text,
        '_Review__timestamp': reviews.c.timestamp,
        '_Review__rating': reviews.c.rating,
        '_Review__user': reviews.c.user
    })
    movies_mapper = mapper(model.Movie, movies, properties={
        '_Movie__id': movies.c.id,
        '_Movie__release_year': movies.c.release_year,
        '_Movie__title': movies.c.title,
        '_Movie__description': movies.c.description,
        '_Movie__director_full_name': movies.c.director_full_name,
        # '_hyperlink': movies.c.hyperlink,
        # '_image_hyperlink': movies.c.image_hyperlink,
        '_Movie__rating': movies.c.rating,
        '_Movie__review_text': relationship(model.Review, backref='_movie'),
        '_Movie__rating_count': movies.c.rating_count
    })
    mapper(model.Genre, tags, properties={
        '_Genre__genre_name': tags.c.genre_name,
        '_Genre__tagged_movies': relationship(
            movies_mapper,
            secondary=movie_tags,
            backref="_genres"
        )
    })

    mapper(model.Actor, actors, properties={
        '_Actor__actor_full_name': actors.c.actor_full_name,
        '_Actor__for_movies': relationship(
            movies_mapper,
            secondary=movie_actors,
            backref="_actors"
        )
    })