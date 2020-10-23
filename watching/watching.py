from flask import Blueprint
from flask import request, render_template, redirect, url_for, session
import random

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import datafilereaders.repository as repo
import watching.services as services

from authentication.authentication import login_required


watching_blueprint = Blueprint(
    'watching_bp', __name__)


@watching_blueprint.route('/movies_by_tag', methods=['GET'])
def movies_by_tag():
    movies_per_page = 8

    # Read query parameters.
    tag_name = request.args.get('tag')
    cursor = request.args.get('cursor')

    # article_to_show_comments = request.args.get('view_comments_for')

    # if article_to_show_comments is None:
    #     # No view-comments query parameter, so set to a non-existent article id.
    #     article_to_show_comments = -1
    # else:
    #     # Convert article_to_show_comments from string to int.
    #     article_to_show_comments = int(article_to_show_comments)

    random_list = []
    for i in range(0, 100):
        n = random.randint(1, 20)
        if n not in random_list:
            random_list.append(n)
        if len(random_list) == 8:
            break
    movie_name_list = []
    for i in range(len(random_list)):
        movie_name_list.append('image/movie' + str(random_list[i]) + '.jpeg')

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    # Retrieve article ids for articles that are tagged with tag_name.
    movies_ids = services.get_movie_ids_by_tags(tag_name, repo.repo_instance)

    # Retrieve the batch of articles to display on the Web page.
    movies = services.get_single_page_of_movies(movies_ids[cursor:cursor + movies_per_page], repo.repo_instance)
    length_of_movies = len(movies)
    first_article_url = None
    last_article_url = None
    next_article_url = None
    prev_article_url = None

    if cursor > 0:
        # There are preceding articles, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_article_url = url_for('watching_bp.movies_by_tag', tag=tag_name, cursor=cursor - movies_per_page)
        first_article_url = url_for('watching_bp.movies_by_tag', tag=tag_name)

    if cursor + movies_per_page * 2 < len(movies_ids):
        # There are further articles, so generate URLs for the 'next' and 'last' navigation buttons.
        next_article_url = url_for('watching_bp.movies_by_tag', tag=tag_name, cursor=cursor + movies_per_page)

        last_cursor = (movies_per_page * int(len(movies_ids) / movies_per_page))-movies_per_page
        if len(movies_ids) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_article_url = url_for('watching_bp.movies_by_tag', tag=tag_name, cursor=last_cursor)

    # Construct urls for viewing article comments and adding comments.
    # for article in articles:
    #     article['view_comment_url'] = url_for('news_bp.articles_by_tag', tag=tag_name, cursor=cursor, view_comments_for=article['id'])
    #     article['add_comment_url'] = url_for('news_bp.comment_on_article', article=article['id'])

    # Generate the webpage to display the articles.
    return render_template(
        'news/articles.html',
        title='Movies',
        movie_title='Movies tagged by ' + tag_name,
        movies=movies,
        length_of_movies = length_of_movies,
        movie_name_list=movie_name_list,
        # selected_articles=utilities.get_selected_articles(len(articles) * 2),
        # tag_urls=utilities.get_tags_and_urls(),
        first_article_url=first_article_url,
        last_article_url=last_article_url,
        prev_article_url=prev_article_url,
        next_article_url=next_article_url,
        # show_comments_for_article=article_to_show_comments
    )