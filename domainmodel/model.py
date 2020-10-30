from datetime import date
from domainmodel.classes_in_model.review import Review


class Actor:

    def __init__(self, actor_full_name: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_full_name.strip()

        self.__actors_this_one_has_worked_with = set()

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    def add_actor_colleague(self, colleague):
        if isinstance(colleague, self.__class__):
            self.__actors_this_one_has_worked_with.add(colleague)

    def check_if_this_actor_worked_with(self, colleague):
        return colleague in self.__actors_this_one_has_worked_with

    def __repr__(self):
        return f'<Actor {self.__actor_full_name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.actor_full_name == self.__actor_full_name

    def __lt__(self, other):
        return self.__actor_full_name < other.actor_full_name

    def __hash__(self):
        return hash(self.__actor_full_name)


class Director:

    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    def __repr__(self):
        return f'<Director {self.__director_full_name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.director_full_name == self.director_full_name

    def __lt__(self, other):
        return self.director_full_name < other.director_full_name

    def __hash__(self):
        return hash(self.__director_full_name)


class Genre:

    def __init__(self, genre_name : str):
        self.__genre_name = None
        if genre_name == "" or type(genre_name) is not str:
            self.__genre_name = None
        else:
            self.__genre_name = genre_name.strip()

        self.__tagged_movies = list()

    @property
    def tagged_movies(self):
        return self.__tagged_movies

    @property
    def genre_name(self) -> str:
        return self.__genre_name

    def add_movie(self, movie):
        self.__tagged_movies.append(movie)

    def __repr__(self):
        return f'<Genre {self.__genre_name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.genre_name == self.__genre_name

    def __lt__(self, other):
        return self.__genre_name < other.genre_name

    def __hash__(self):
        return hash(self.__genre_name)


class Movie:

    def __init__(self, title: str, release_year: int):
        self.__release_year = None
        self.__title = None

        if release_year >= 1900 and type(release_year) is int:
            self.__release_year = release_year

        if title.strip() == "" or type(title) is not str:
            self.__title = None
        else:
            self.__title = title.strip()
        self.__rating: float = 0.0
        self.__rating_count = 0
        self.__id: int = id
        self.__image_url = None
        self.__description = None
        self.__director = None
        self.__actors = []
        self.__genres = []
        self.__runtime_minutes = None
        self.__review = list()
    # essential attributes



    @property
    def rating(self) -> int:
        return self.__rating

    @rating.setter
    def rating(self, number: float):
        new_total = self.rating * self.rating_count + number
        print('new tital')
        print(new_total)
        self.__rating_count += 1
        self.__rating = round((new_total) / float(self.rating_count), 1)
        print('finall check')
        print(self.__rating)

    @property
    def rating_count(self) -> int:
        return self.__rating_count

    @property
    def id(self) -> int:
        return self.__id

    @property
    def review(self):
        return self.__review

    @property
    def image_url(self) -> str:
        return self.__image_url

    @image_url.setter
    def image_url(self, url: str):
        self.__image_url = url

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, title: str):
        self.__title = title

    @id.setter
    def id(self, id: str):
        self.__id = id

    @property
    def release_year(self) -> int:
        return self.__release_year

    @release_year.setter
    def release_year(self, release_year: int):
        self.__release_year = release_year

    # additional attributes

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str):
        if type(description) is str:
            self.__description = description.strip()
        else:
            self.__description = None

    @property
    def director(self) -> Director:
        return self.__director

    @director.setter
    def director(self, director: Director):
        if isinstance(director, Director):
            self.__director = director
        else:
            self.__director = None

    def add_review(self, review: Review):
        self.__review.append(review)

    @property
    def actors(self) -> list:
        return self.__actors

    def __change_rating__(self, rating_number, number_of_cutting_count):
        if type(rating_number) == float and 0 < rating_number < 11:
            self._rating = rating_number
            if number_of_cutting_count <= self._rating_count and type(number_of_cutting_count) == int:
                self._rating_count -= number_of_cutting_count

    def add_actor(self, actor: Actor):
        if not isinstance(actor, Actor) or actor in self.__actors:
            return

        self.__actors.append(actor)

    def remove_actor(self, actor: Actor):
        if not isinstance(actor, Actor):
            return

        try:
            self.__actors.remove(actor)
        except ValueError:
            # print(f"Movie.remove_actor: Could not find {actor} in list of actors.")
            pass

    @property
    def genres(self) -> list:
        return self.__genres

    def add_genre(self, genre: Genre):
        if not isinstance(genre, Genre) or genre in self.__genres:
            return

        self.__genres.append(genre)

    def remove_genre(self, genre: Genre):
        if not isinstance(genre, Genre):
            return

        try:
            self.__genres.remove(genre)
        except ValueError:
            # print(f"Movie.remove_genre: Could not find {genre} in list of genres.")
            pass

    @property
    def runtime_minutes(self) -> int:
        return self.__runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, val: int):
        if val > 0:
            self.__runtime_minutes = val
        else:
            raise ValueError(f'Movie.runtime_minutes setter: Value out of range {val}')

    def __get_unique_string_rep(self):
        return f"{self.__title}, {self.__release_year}"

    def __repr__(self):
        return f'<Movie {self.__get_unique_string_rep()}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__get_unique_string_rep() == other.__get_unique_string_rep()

    def __lt__(self, other):
        if self.title == other.title:
            return self.release_year < other.release_year
        return self.title < other.title

    def __hash__(self):
        return hash(self.__get_unique_string_rep())


class Review:

    def __init__(self, movie: Movie, review_text: str, rating: int):
        if isinstance(movie, Movie):
            self.__movie = movie
        else:
            self.__movie = None
        if type(review_text) is str:
            self.__review_text = review_text
        else:
            self.__review_text = None

        if type(rating) is int and rating >= 1 and rating <= 10:
            self.__rating = rating
        else:
            self.__rating = None
        self.__timestamp = date.today()
        self.__user = None
        self.__movie_id = None

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, username: str):
        self.__user = username

    @property
    def movie_id(self):
        return self.__movie_id

    @movie_id.setter
    def movie_id(self, id: int):
        self.__movie_id = id


    @property
    def movie(self) -> Movie:
        return self.__movie

    @property
    def review_text(self) -> str:
        return self.__review_text

    @property
    def rating(self) -> int:
        return self.__rating

    @property
    def timestamp(self) -> date:
        return self.__timestamp

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.movie == self.__movie and other.review_text == self.__review_text and other.rating == self.__rating and other.timestamp == self.__timestamp

    def __repr__(self):
        return f'<Review of movie {self.__movie_id}, rating = {self.__rating}, timestamp = {self.__timestamp}>'


class User:

    def __init__(self, username: str, password: str):
        self.__username = None
        self.__password = None
        if username == "" or type(username) is not str:
            self.__username = None
        else:
            self.__username = username.strip().lower()
        if password == "" or type(password) is not str:
            self.__password = None
        else:
            self.__password = password
        self.__watched_movies = list()
        self.__reviews = list()
        self.__time_spent_watching_movies_minutes = 0

    @property
    def username(self) -> str:
        return self.__username

    @property
    def password(self) -> str:
        return self.__password

    @property
    def watched_movies(self) -> list:
        return self.__watched_movies

    @property
    def reviews(self) -> list:
        return self.__reviews

    @property
    def time_spent_watching_movies_minutes(self) -> int:
        return self.__time_spent_watching_movies_minutes

    def watch_movie(self, movie: Movie):
        if isinstance(movie, Movie):
            self.__watched_movies.append(movie)
            self.__time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review: Review):
        if isinstance(review, Review):
            self.__reviews.append(review)

    def __repr__(self):
        return f'<User {self.__username}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.username == self.__username

    def __lt__(self, other):
        return self.__username < other.user_name

    def __hash__(self):
        return hash(self.__username)


class WatchList:
    def __init__(self):
        self._watch_list = []
        self._index = 0

    def add_movie(self, movie):
        if not isinstance(movie, Movie) or movie in self._watch_list:
            pass
        else:
            self._watch_list.append(movie)

    def remove_movie(self, movie):
        if not isinstance(movie, Movie) or movie not in self._watch_list:
            pass
        else:
            self._watch_list.remove(movie)

    def select_movie_to_watch(self, index):
        if len(self._watch_list) == 0:
            return None
        if len(self._watch_list) - 1 >= index >= 0:
            return self._watch_list[index]
        else:
            return None

    def size(self):
        return len(self._watch_list)

    def first_movie_in_watchlist(self):
        if len(self._watch_list) == 0:
            return None
        else:
            return self._watch_list.__getitem__(0)

    @property
    def watch_list(self):
        return self._watch_list

    def __iter__(self):
        return self

    def __next__(self):
        if self._index == len(self._watch_list):
            raise StopIteration
        self._index += 1
        return self._watch_list[self._index - 1]


def make_review(review_text: str, user: User, movie: Movie, rating: str):
    review = Review(movie, review_text, rating)
    user.add_review(review)
    movie.add_review(review)
    return review



