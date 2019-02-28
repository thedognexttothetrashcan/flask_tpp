from App.ext import cache
from App.models.admin import AdminUser
from App.models.cinema.user_model import CinemaUser
from App.utils.token_utils import ADMIN, CINEMA


def get_admin_user(token):

    if token:

        if token.startswith(ADMIN):

            user_id = cache.get(token)

            if user_id:
                user = AdminUser.query.get(user_id)

                if user:
                    return user

    return None


def get_cinema_user(token):
    if token:

        if token.startswith(CINEMA):

            user_id = cache.get(token)

            if user_id:
                user = CinemaUser.query.get(user_id)

                if user:
                    return user

    return None
