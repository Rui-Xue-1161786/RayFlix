from flask import Blueprint, request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
import datafilereaders.repository as repo
from wtforms import SelectField, SubmitField, StringField
from wtforms.validators import DataRequired, InputRequired

utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_tags_and_urls():
    # get genre_dictionary
    tag_names = repo.repo_instance.get_genre()
    tag_urls = dict()
    for tag_name in tag_names:
        tag_urls[tag_name] = url_for('watching_bp.movies_by_tag', tag=tag_name)
    return tag_urls


class RatingForm(FlaskForm):
    number = SelectField('Rating', choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], validators=[DataRequired()])
    submit = SubmitField('Submit')
    review = StringField('review',validators=[InputRequired('Input required!')])


