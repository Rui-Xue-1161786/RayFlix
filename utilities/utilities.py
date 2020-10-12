from flask import Blueprint, request, render_template, redirect, url_for, session

import utilities.services as services
import datafilereaders.repository as repo

# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_genres_and_urls():
    genres_names = services.get_genre_names(repo.repo_instance)
    genres_urls = dict()
    for genre_name in genres_names:
        genres_urls[genre_name] = url_for('watching_bp.movies_by_tag', genre=genre_name)

    return genres_urls


@utilities_blueprint.route('/video', methods=['GET'])
def video():
    # number_of_movie = repo.repo_instance.get_number_of_movies()
    # genre_list = repo.repo_instance.get_genre()

    return render_template(
        'video/video.html'
        # number=number_of_movie,
        # genre_list = genre_list

    )


# def get_selected_movies(quantity=3):
#     movies = services.get_random_movies(quantity, repo.repo_instance)
#
#     for movie in movies:
#         movie['hyperlink'] = url_for('watching_bp.movies_by_year', year=movie['release_year'].isoformat())
#     return movies
