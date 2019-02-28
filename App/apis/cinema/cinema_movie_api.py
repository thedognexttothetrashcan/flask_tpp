
from flask import request, g
from flask_restful import Resource, abort

from App.apis.cinema.decorator import login_required
from App.models.cinema.cinema_user_movie_model import CinemaUserMovie


class CinemaMoviesResource(Resource):

    @login_required
    def post(self):

        movie_id = request.form.get("movie_id")

        cinema_movie = CinemaUserMovie()

        cinema_movie.c_movie_id = movie_id

        cinema_movie.c_cinema_user = g.user.id

        if not cinema_movie.save():
            abort(400, msg="购买失败")
        data = {
            "msg": "ok",
            "status": 201,
            "pay_url": "xxx"
        }

        return data

