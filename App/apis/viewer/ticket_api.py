from flask_restful import Resource
from sqlalchemy import func

from App.ext import db
from App.models.cinema.paidang_model import PaiDang
from App.models.common.movie_model import Movie
from App.models.viewer.seat_order_model import SeatOrder


class TicketsResource(Resource):

    def get(self):

        print(Movie.query)

        print(type(Movie.query))

        movies_top = db.session.query(Movie.id, Movie.m_name, func.sum(SeatOrder.s_price))\
            .join(Movie.m_paidangs).join(PaiDang.seatorders).group_by(Movie.id).order_by(-func.sum(SeatOrder.s_price))

        print(movies_top)

        for movie_top in movies_top:
            print(movie_top)

        return {"msg": "ok"}
