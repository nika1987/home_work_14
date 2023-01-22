from flask import Blueprint, jsonify
from utils import get_data, get_movies, get_movie_rating, get_movie_desc
from constants import DB_TABLE

main_blueprint = Blueprint("main_blueprint", __name__)



@main_blueprint.route("/movie/<title>/")
def page_movie(title: str):
    queue = f"""
     SELECT * 
     FROM {DB_TABLE}
     WHERE title = '{title}'
     ORDER BY date_added desc 
     """

    queue_result = get_data(queue)

    if queue_result is None:
        return jsonify(status=404)

    movie = {
        "title": queue_result['title'],
        "country": queue_result['country'],
        "release_year": queue_result['release_year'],
        "genre": queue_result['genre'],
        "description": queue_result['description']
    }

    return jsonify(movie)


@main_blueprint.route("/movie/<int:year>/to/<int:end_year>")
def page_movies(year, end_year):
    return jsonify(get_movies(year, end_year))


@main_blueprint.route("/rating/<age>")
def page_rating(age):
    return jsonify(get_movie_rating(age))


@main_blueprint.route("/genre/<genre>")
def page_listed(genre):
    return jsonify(get_movie_desc(genre))
