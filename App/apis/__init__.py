from App.apis.admin import admin_api
from App.apis.cinema import cinema_api
from App.apis.common import common_api
from App.apis.viewer import viewer_api


def init_api(app):
    admin_api.init_app(app)
    cinema_api.init_app(app)
    viewer_api.init_app(app)
    common_api.init_app(app)