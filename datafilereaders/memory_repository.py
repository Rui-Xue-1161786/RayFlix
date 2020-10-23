from domainmodel.model import Movie, Genre, User, Review,Actor, WatchList, Director
from datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from datafilereaders.repository import AbstractRepository
from typing import List
import random

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

    def get_all_movie(self):
        return self._movie

    def add_user(self, user: User):
        self._user.append(user)

    def get_user(self, username) -> User:
        return next((the_user for the_user in self._user if the_user.username == username), None)

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

    def get_movie_ids_for_genre(self, genre_name: str):
        # Linear search, to find the first occurrence of a Tag with the name tag_name.
        # genre = next((genre for genre in self._genre if genre.genre_name == genre_name), None)

        movie_ids = list()
        for movie in self._movie:
            if Genre(genre_name) in movie.genres:
                movie_ids.append(movie.id)
        return movie_ids

    def add_review(self, review: Review):
        self._review.append(review)

    def get_review(self):
        return self._review

    def add_movie(self, movie: Movie):
        self._movie.append(movie)

    def get_movie(self, title: str, release_year: int) -> Movie:
        return next((the_movie for the_movie in self._movie if
                     the_movie.title == title and the_movie.release_year == release_year), None)

    def get_number_of_movies(self):
        return len(self._movie)

    def get_movie_by_id(self, id:int):
        movie = None

        for film in self._movie:

            if id == film.id:
                movie = film

        return movie

    def get_movie_list_by_id_list(self, id_list):
        movie_list = []
        for movie in self._movie:
            if movie.id in id_list:
                movie_list.append(movie)
        return movie_list

    def get_movie_by_name(self, title: str):
        return next((the_movie for the_movie in self._movie if
                     the_movie.title == title), None)





filename = '/Users/rayxue/Downloads/RayFlix-master/datafiles/Data1000Movies.csv'
repo = MemoryRepository(filename)
same_name = []
for movie in repo.get_all_movie():
    movie_name = movie.title
    count = 1
    for i in repo.get_all_movie():
        if movie_name == i.title:
            count += 1
        if count == 3:
            if movie_name not in same_name:
                same_name.append(movie_name)
print(same_name)

for movie in repo.get_all_movie():
    if movie.title == 'The Host':
        print(movie)



# id_list = repo.get_movie_ids_for_genre("Sci-Fi")
# print(id_list)
# print(repo.get_movie_list_by_id_list(id_list))

# all_movie = repo.get_all_movie()
# family_list = []
# tag_family = Genre('Family')
# print(tag_family)









