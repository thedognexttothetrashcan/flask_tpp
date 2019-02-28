from flask_restful import Api

from App.apis.cinema.cinema_api import CinemasResource, CinemaResource
from App.apis.cinema.cinema_movie_api import CinemaMoviesResource
from App.apis.cinema.hall_api import HallsResource
from App.apis.cinema.order_api import OrdersResource
from App.apis.cinema.order_status_api import OrderStatusResource
from App.apis.cinema.paidang_api import PaiDangsResource
from App.apis.cinema.user_api import CinemaUsersResource

cinema_api = Api(prefix="/cinema")

cinema_api.add_resource(CinemaUsersResource, "/users/")

cinema_api.add_resource(CinemasResource, "/cinemas/")
cinema_api.add_resource(CinemaResource, "/cinemas/<int:pk>/")

cinema_api.add_resource(OrdersResource, "/orders/")

cinema_api.add_resource(OrderStatusResource, "/orderstatus/")

cinema_api.add_resource(CinemaMoviesResource, "/cinemamovies/")

cinema_api.add_resource(HallsResource, "/halls/")

cinema_api.add_resource(PaiDangsResource, "/paidangs/")