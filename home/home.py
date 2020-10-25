
import random
from flask import Blueprint, render_template, request, url_for, session, flash, redirect
import datafilereaders.repository as repo
from authentication.authentication import SearchForm
from domainmodel.model import Movie, Review
import utilities.utilities as utilities


home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    if form.is_submitted():
        movie_name = request.form['search_information']

        try:

            movies = repo.repo_instance.get_movie_by_name(movie_name)

        except:
            pass
        #find movie by actor

        if len(movies) == 0:
            movies.append(Movie('No Result, Please Try Another Name !', 0))
        length_of_movies = len(movies)

        return render_template(
            'search/search.html',
            movie_list=movies,
            length_of_movies=length_of_movies

        )

    # number_of_movie = repo.repo_instance.get_number_of_movies()

    movie = Movie("A_movie", 2008)

    random_list = []
    my_movie_id_list = []
    for i in range(0, 100):
        n = random.randint(1, 20)
        if n not in random_list:
            random_list.append(n)
            my_movie_id_list.append(n)
        if len(random_list) == 8:
            break
    movie_name_list = []
    for i in range(len(random_list)):
        movie_name_list.append('image/movie' + str(random_list[i]) + '.jpeg')
    the_movie_name_list = repo.repo_instance.get_movie_list_by_id_list(my_movie_id_list)
    length_of_movies = 8
    return render_template(
        'home/home.html',
        movie=movie,
        form=form,
        the_movie_name_list=the_movie_name_list,
        tag_urls=utilities.get_tags_and_urls(),
        movie_name_list=movie_name_list,
        length_of_movies=length_of_movies
    )


@home_blueprint.route('/video/<string:movie>', methods=['GET', 'POST'])
def video(movie):
    # number_of_movie = repo.repo_instance.get_number_of_movies()
    # genre_list = repo.repo_instance.get_genre
    try:
        movies = repo.repo_instance.get_movie_by_name(movie)
        my_movie = movies[0]
        my_movie.rating = 7.5
    except:
        my_movie = Movie('No_Result',0)
        my_movie.rating = 7.5
    if "username" in session:
        form = utilities.RatingForm()


        # Successful POST, i.e. the username and password have passed validation checking.
        # Use the service layer to attempt to add the new user.
        if request.method == 'POST':

                b = 0
                for i in range(11):
                    if i == int(form.number.data):
                        b = i
                text = form.review.data
                review = Review(my_movie, text, b)
                repo.repo_instance.add_review(review)

                # All is well, redirect the user to the login page.
                flash('Successful Rating !')
                # return redirect(url_for('home_bp.video',movie=movie))
                return render_template(
                    'video/video.html',
                    movie = my_movie)
            # except:
            #     print("faild!!!!!!")
            #     flash('Something Wrong, please try again !', "info")

        return render_template(
            'video/video_with_review.html',
            form=form,
            movie = my_movie
        )

    return render_template(
        'video/video.html',
        movie=my_movie,
        tag_urls=utilities.get_tags_and_urls()
        # number=number_of_movie,
        # genre_list = genre_list

    )
