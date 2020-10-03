from domainmodel.actor import Actor
from domainmodel.director import Director
from domainmodel.genre import Genre
from domainmodel.movie import Movie
from domainmodel.review import Review
from domainmodel.user import User
from datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from datafilereaders.repository import AbstractRepository
from typing import List


class MemoryRepository(AbstractRepository):

    def __init__(self, file_path: str):
        movie_file_reader = MovieFileCSVReader(file_path)
        movie_file_reader.read_csv_file()
        self._actor = movie_file_reader.dataset_of_actors
        self._director = movie_file_reader.dataset_of_directors
        self._genre = movie_file_reader.dataset_of_genres
        self._movie = movie_file_reader.dataset_of_movies
        self._user = list()
        self._review = list()

    def add_user(self, user: User):
        self._user.append(user)

    def get_user(self, username) -> User:
        return next((the_user for the_user in self._user if the_user.user_name == username), None)

    def add_actor(self, actor: Actor):
        self._actor.add(actor)

    def get_actor(self, actor: str) -> Actor:
        return next((the_actor for the_actor in self._actor if the_actor.actor_full_name == actor), None)

    def add_director(self, director: Director):
        self._director.add(director)

    def get_director(self, director: str) -> Director:
        return next((the_dire for the_dire in self._director if the_dire.director_full_name == director), None)

    @property
    def get_director_list(self):
        return self._director

    def add_genre(self, genre: Genre):
        self._genre.add(genre)

    def get_genre(self) -> List[Genre]:
        return self._genre

    def add_review(self, review: Review):
        self._review.append(review)

    def get_review(self):
        return self._review

    def add_movie(self, movie: Movie):
        self._movie.append(movie)

    def get_movie(self, title: str, release_year: int) -> Movie:
        return next((the_movie for the_movie in self._movie if the_movie.title == title and the_movie.release_year == release_year), None)

# filename = '/Users/rayxue/Downloads/RayFlix-master/datafiles/Data1000Movies.csv'
# repo = MemoryRepository(filename)
# print(len(repo.get_genre()))
#
# print(next((the_genre for the_genre in repo.get_genre() if the_genre == Genre('Rayyy')), None))



