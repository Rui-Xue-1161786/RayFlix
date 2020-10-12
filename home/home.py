from flask import Blueprint, render_template
import datafilereaders.repository as repo
# import covid.utilities.utilities as utilities


home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    number_of_movie = repo.repo_instance.get_number_of_movies()
    genre_list = repo.repo_instance.get_genre()

    return render_template(
        'home/home.html',
        number=number_of_movie,
        genre_list = genre_list

    )


@home_blueprint.route('/video', methods=['GET'])
def video():
    # number_of_movie = repo.repo_instance.get_number_of_movies()
    # genre_list = repo.repo_instance.get_genre

    return render_template(
        'video/video.html'
        # number=number_of_movie,
        # genre_list = genre_list

    )