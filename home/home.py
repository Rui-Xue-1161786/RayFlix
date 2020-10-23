from flask import Blueprint, render_template, request
import datafilereaders.repository as repo
from authentication.authentication import SearchForm



home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET','POST'])
def home():
    form = SearchForm()
    if form.is_submitted():
        movie_name = request.form['search_information']
        # try:
        #     repo.get_movie()
        return render_template(
            'family/family.html',
            movie_name=movie_name
        )

    # number_of_movie = repo.repo_instance.get_number_of_movies()
    genre_list = repo.repo_instance.get_genre()

    return render_template(
        'home/home.html',
        form=form,
        # number=number_of_movie,
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