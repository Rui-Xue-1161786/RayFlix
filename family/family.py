from domainmodel.model import Movie, Genre, User, Review,Actor, WatchList, Director
from flask import Blueprint, render_template
import datafilereaders.repository as repo
# # import covid.utilities.utilities as utilities
# import family.services as services

family_blueprint = Blueprint(
    'family_bp', __name__)


@family_blueprint.route('/family', methods=['GET'])
def family():

    all_movie = repo.repo_instance.get_all_movie()
    family_list = []
    tag_family = Genre('Family')
    for movie in all_movie:
        for i in movie.genres:
            if tag_family.__repr__() == i.__repr__():
                family_list.append(movie)

    return render_template(
        "family/family.html",
        family_list=family_list
    )