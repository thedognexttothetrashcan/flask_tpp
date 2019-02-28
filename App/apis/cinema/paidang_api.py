from flask import g
from flask_restful import Resource, reqparse, abort, fields, marshal, marshal_with
from sqlalchemy import or_, and_

from App.apis.cinema.decorator import login_required
from App.models.cinema.cinema_model import Cinema
from App.models.cinema.cinema_user_movie_model import CinemaUserMovie
from App.models.cinema.paidang_model import PaiDang
from App.models.common.movie_model import Movie
from App.utils.date_time_utils import calc_time

parse = reqparse.RequestParser()
parse.add_argument("movie_id", required=True, help="请选择电影")
parse.add_argument("hall_id", required=True, help="请选择放映厅")
parse.add_argument("price", required=True, help="请录入价钱")
parse.add_argument("time_start", required=True, help="请选择时间")

paidang_fields ={
    "p_movie": fields.Integer,
    "p_hall": fields.Integer,
    "p_price": fields.Float,
    "p_time_start": fields.DateTime,
    "p_time_end": fields.DateTime
}

single_paidang_fields = {
    "msg": fields.String,
    "status": fields.Integer,
    "data": fields.Nested(paidang_fields)
}

multi_paidang_fields = {
    "msg": fields.String,
    "status": fields.Integer,
    "data": fields.List(fields.Nested(paidang_fields))
}

paidang_parse = reqparse.RequestParser()
paidang_parse.add_argument("movie_id", required=True, help="请选择电影")
paidang_parse.add_argument("cinema_id", required=True, help="请选择影院")
paidang_parse.add_argument("see_date", required=True, help="请选择日期")


class PaiDangsResource(Resource):

    @marshal_with(multi_paidang_fields)
    def get(self):

        args = paidang_parse.parse_args()

        movie_id = args.get("movie_id")

        see_date_0 = args.get("see_date") + " 00:00:00"

        see_date_24 = args.get("see_date") + " 23:59:59"

        cinema_id = args.get("cinema_id")   # 需要   hall.id   一个电影院多个大厅

        #  电影名  电影院   日期  区域（可选）(没有真实作用，限制影院选取的)

        cinema = Cinema.query.get(cinema_id)

        halls = cinema.halls

        hall_ids = [hall.id for hall in halls]

        paidangs = PaiDang.query.filter(PaiDang.p_movie == movie_id).filter(PaiDang.p_time_start > see_date_0)\
            .filter(PaiDang.p_time_start < see_date_24)\
            .filter(PaiDang.p_hall.in_(hall_ids))

        data = {
            "msg": "ok",
            "status": 200,
            "data": paidangs
        }

        return data

    @login_required
    def post(self):

        args = parse.parse_args()
        movie_id = args.get("movie_id")
        hall_id = args.get("hall_id")
        price = args.get("price")
        time_start = args.get("time_start")

        # movie_id 是否购买
        cinema_user_movies = CinemaUserMovie.query.filter_by(c_movie_id=movie_id).filter_by(c_cinema_user=g.user.id).all()

        print(cinema_user_movies)

        if not cinema_user_movies:
            abort(403, msg="错误排挡")

        movie = Movie.query.get(movie_id)
        duration = movie.m_duration

        # 条件， 开始时间不能在时间段之内，  结束时间不能在时间段内， 电影时间不能是子集
        # 基于放映厅
        time_end = calc_time(time_start, duration)
        # 条件 应该是取出  在开始和结束时间之间的电影
        paidangs = PaiDang.query.filter_by(p_hall=hall_id).\
            filter(or_(and_(PaiDang.p_time_start > time_start, PaiDang.p_time_start < time_end),
                       and_(PaiDang.p_time_end > time_start, PaiDang.p_time_end < time_end)))

        print(paidangs)

        paidangs = paidangs.all()

        if paidangs:
            abort(400, msg="此时间已存在排挡")

        paidangs = PaiDang.query.filter_by(p_hall=hall_id).filter(and_(PaiDang.p_time_start < time_start, PaiDang.p_time_end > time_end))

        print(paidangs)

        paidangs = paidangs.all()

        if paidangs:
            abort(400, msg="被包含型排挡")

        paidang = PaiDang()
        paidang.p_hall = hall_id
        paidang.p_movie = movie_id
        paidang.p_price = price
        paidang.p_time_start = time_start
        paidang.p_time_end = time_end

        if not paidang.save():
            abort(400, msg="排挡失败")

        data = {
            "msg": "ok",
            "status": 201,
            "data": paidang
        }

        return marshal(data, single_paidang_fields)