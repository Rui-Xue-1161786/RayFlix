from domainmodel.movie import Movie


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


watchlist = WatchList()
movie1 = Movie("Moana", 2016)
watchlist.add_movie(movie1)
watchlist.add_movie(Movie("Ice Age", 2909))
watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
a = iter(watchlist)
print(a.__next__())
print(a.__next__())
print(a.__next__())