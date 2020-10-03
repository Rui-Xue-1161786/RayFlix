from __init__ import create_app
from datafilereaders.movie_file_csv_reader import MovieFileCSVReader


def main():
    file_path = '/Users/rayxue/Downloads/RayFlix-master/datafiles/Data1000Movies.csv'
    movie_file_reader = MovieFileCSVReader(file_path)
    movie_file_reader.read_csv_file()
    app = create_app()
    app.run(host='localhost', port=5000)


if __name__ == "__main__":
    main()