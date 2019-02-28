from flask import request
from flask_restful import Resource, marshal_with, fields, reqparse, abort, marshal

from App.apis.admin.decorator import login_required
from App.models.common.movie_model import Movie

movie_fields = {
    "m_name": fields.String,
    "m_name_en": fields.String,
    "m_director": fields.String,
    "m_leading_role": fields.String,
    "m_duration": fields.Integer,
    "m_country": fields.String,
    "m_type": fields.String,
    "m_screen_model": fields.String,
    "m_introduce": fields.String,
    "m_open_day": fields.DateTime
}

multi_movie_fields = {
    "msg": fields.String,
    "status": fields.Integer,
    "data": fields.List(fields.Nested(movie_fields))
}

single_movie_fields = {
    "msg": fields.String,
    "status": fields.Integer,
    "data": fields.Nested(movie_fields)
}

parse = reqparse.RequestParser()
parse.add_argument("m_name", required=True, help="请提供电影名")
parse.add_argument("m_name_en", required=True, help="请提供英文电影名")
parse.add_argument("m_director", required=True, help="请填写导演")
parse.add_argument("m_leading_role", required=True, help="请提供主演")
parse.add_argument("m_duration", type=int, required=True, help="请提供时长")
parse.add_argument("m_country", required=True, help="请提供国家")
parse.add_argument("m_type", required=True, help="请提供类型")
parse.add_argument("m_screen_model", required=True, help="请提供荧屏模型")
parse.add_argument("m_introduce", required=True, help="请提供描述")
parse.add_argument("m_open_day", required=True, help="请选择上映日期")


class MoviesResource(Resource):

    @marshal_with(multi_movie_fields)
    def get(self):
        movies = Movie.query.all()

        data = {
            "msg": "ok",
            "status": 200,
            "data": movies
        }

        return data

    @login_required
    def post(self):

        args = parse.parse_args()

        m_name = args.get("m_name")
        m_name_en = args.get("m_name_en")
        m_director = args.get("m_director")
        m_leading_role = args.get("m_leading_role")
        m_duration = args.get("m_duration")
        m_country = args.get("m_country")
        m_type = args.get("m_type")
        m_screen_model = args.get("m_screen_model")
        m_introduce = args.get("m_introduce")
        m_open_day = args.get("m_open_day")

        movie = Movie()
        movie.m_name = m_name
        movie.m_name_en = m_name_en
        movie.m_director = m_director
        movie.m_leading_role = m_leading_role
        movie.m_duration = m_duration
        movie.m_country = m_country
        movie.m_type = m_type
        movie.m_screen_model = m_screen_model
        movie.m_introduce = m_introduce
        movie.m_open_day = m_open_day

        if not movie.save():
            abort(400, msg="电影添加失败")

        data = {
            "msg": "ok",
            "status": 201,
            "data": movie
        }

        return marshal(data, single_movie_fields)


class MovieResource(Resource):

    def get_obj(self, pk):

        movie = Movie.query.get(pk)

        if not movie:
            abort(400, msg="movie doesn't exist")
        return movie

    @marshal_with(single_movie_fields)
    def get(self, pk):
        movie = self.get_obj(pk)

        data = {
            "msg": "ok",
            "status": 200,
            "data": movie
        }

        return data

    @login_required
    def delete(self, pk):
        movie = self.get_obj(pk)

        if not movie.delete_logic():
            abort(400, msg="删除失败")
        data = {
            "msg": "ok",
            "status": 204
        }

        return data

    @login_required
    def patch(self, pk):

        movie = self.get_obj(pk)

        m_name = request.form.get("m_name")
        m_name_en = request.form.get("m_name_en")
        m_director = request.form.get("m_director")
        m_leading_role = request.form.get("m_leading_role")
        m_duration = request.form.get("m_duration")
        m_country = request.form.get("m_country")
        m_type = request.form.get("m_type")
        m_screen_model = request.form.get("m_screen_model")
        m_introduce = request.form.get("m_introduce")
        m_open_day = request.form.get("m_open_day")

        movie.m_name = m_name or movie.m_name
        movie.m_name_en = m_name_en or movie.m_name_en
        movie.m_director = m_director or movie.m_director
        movie.m_leading_role = m_leading_role or movie.m_leading_role
        movie.m_duration = m_duration or movie.m_duration
        movie.m_country = m_country or movie.m_country
        movie.m_type = m_type or movie.m_type
        movie.m_screen_model = m_screen_model or movie.m_screen_model
        movie.m_introduce = m_introduce or movie.m_introduce
        movie.m_open_day = m_open_day or movie.m_open_day

        if not movie.save():
            abort(400, msg="信息修改失败")

        data = {
            "msg": "ok",
            "status": 201,
            "data": movie
        }

        return marshal(data, single_movie_fields)